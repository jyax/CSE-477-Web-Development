import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import datetime
import os
import time

class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'

    def query(self, query = "SELECT CURDATE()", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    def about(self, nested=False):    
        query = """select concat(col.table_schema, '.', col.table_name) as 'table',
                          col.column_name                               as column_name,
                          col.column_key                                as is_key,
                          col.column_comment                            as column_comment,
                          kcu.referenced_column_name                    as fk_column_name,
                          kcu.referenced_table_name                     as fk_table_name
                    from information_schema.columns col
                    join information_schema.tables tab on col.table_schema = tab.table_schema and col.table_name = tab.table_name
                    left join information_schema.key_column_usage kcu on col.table_schema = kcu.table_schema
                                                                     and col.table_name = kcu.table_name
                                                                     and col.column_name = kcu.column_name
                                                                     and kcu.referenced_table_schema is not null
                    where col.table_schema not in('information_schema','sys', 'mysql', 'performance_schema')
                                              and tab.table_type = 'BASE TABLE'
                    order by col.table_schema, col.table_name, col.ordinal_position;"""
        results = self.query(query)
        if nested == False:
            return results

        table_info = {}
        for row in results:
            table_info[row['table']] = {} if table_info.get(row['table']) is None else table_info[row['table']]
            table_info[row['table']][row['column_name']] = {} if table_info.get(row['table']).get(row['column_name']) is None else table_info[row['table']][row['column_name']]
            table_info[row['table']][row['column_name']]['column_comment']     = row['column_comment']
            table_info[row['table']][row['column_name']]['fk_column_name']     = row['fk_column_name']
            table_info[row['table']][row['column_name']]['fk_table_name']      = row['fk_table_name']
            table_info[row['table']][row['column_name']]['is_key']             = row['is_key']
            table_info[row['table']][row['column_name']]['table']              = row['table']
        return table_info

    def createTables(self, purge=False, data_path='flask_app/database/'):

        # If purge is True, drop existing tables
        if purge:
            # Drop tables in the reverse order of creation because of foreign key constraints
            self.query("DROP TABLE IF EXISTS skills;")
            print("Dropped table: skills")

            self.query("DROP TABLE IF EXISTS experiences;")
            print("Dropped table: experiences")

            self.query("DROP TABLE IF EXISTS positions;")
            print("Dropped table: positions")

            self.query("DROP TABLE IF EXISTS institutions;")
            print("Dropped table: institutions")

            self.query("DROP TABLE IF EXISTS feedback;")
            print("Dropped table: feedback")

        table_creation_order = ['institutions.sql', 'positions.sql', 'experiences.sql', 'skills.sql']
        # Create tables in the predefined order
        for table in table_creation_order:
            table_name = os.path.splitext(table)[0]

            with open(os.path.join(data_path + 'create_tables/', table), 'r') as file:
                current_table = file.read()
                self.query(current_table)
                print(f"Created table: {table_name}")

        # Create the remaining tables not in the predefined list
        for table in os.listdir(data_path + 'create_tables/'):
            if table not in table_creation_order:
                table_name = os.path.splitext(table)[0]
                with open(os.path.join(data_path + 'create_tables/', table), 'r') as file:
                    current_table = file.read()
                    self.query(current_table)
                    print(f"Created new table: {table_name}")

        table_initial_order = ['institutions.csv', 'positions.csv', 'experiences.csv', 'skills.csv']

        for table in table_initial_order:
            print(f"Grabbing info from ordered table list: {table}")
            table_name = os.path.splitext(table)[0]
            print(f"Inserting into {table_name}, with info from ordered table list")
            with open(os.path.join(data_path + 'initial_data/', table), 'r') as file:
                reader = csv.reader(file)
                columns = next(reader)
                for row in reader:
                    row = [None if item == 'NULL' else item for item in row]  # Replace 'NULL' string with None
                    self.insertRows(table_name, columns, [row])
                    print("Calling Insert Function...")
        print("Finished inserting into resume specific tables")

        # Insert data for all CSV files without caring about order
        for table in os.listdir(data_path + 'initial_data/'):
            print(f"Grabbing info from: {table}")
            if table not in table_initial_order:
                table_name = os.path.splitext(table)[0]
                print(f"Inserting into: {table_name}")
                with open(os.path.join(data_path + 'initial_data/', table), 'r') as file:
                    reader = csv.reader(file)
                    columns = next(reader)
                    for row in reader:
                        row = [None if item == 'NULL' else item for item in row]  # Replace 'NULL' string with None
                        self.insertRows(table_name, columns, [row])
                        print("Calling Insert function...")
        print("All finished!")

    def insertRows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):
        for parameter in parameters:
            query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in parameter])})"
            self.query(query, parameter)
        print(f"Inserted into table {table}.")

    def getResumeData(self):
        # Pulls data from the database to genereate data like this:
        institutions = self.query(f"SELECT * FROM institutions")
        resume_data = {}

        institutions_and_positions_query = """
                SELECT i.*, p.*
                FROM institutions i
                LEFT JOIN positions p ON i.inst_id = p.inst_id
                """
        institutions_and_positions = self.query(institutions_and_positions_query)

        for row in institutions_and_positions:
            inst_id = row['inst_id']

            if inst_id not in resume_data:
                resume_data[inst_id] = {
                    'address': row['address'],
                    'city': row['city'],
                    'state': row['state'],
                    'type': row['type'],
                    'zip': row['zip'],
                    'department': row['department'],
                    'name': row['name'],
                    'positions': {}
                }

            if row['pos_id']:
                pos_id = row['pos_id']
                resume_data[inst_id]['positions'][pos_id] = {
                    'end_date': row['end_date'],
                    'responsibilities': row['responsibilities'],
                    'start_date': row['start_date'],
                    'title': row['title'],
                    'experiences': {}
                }

                # Using JOINs to get positions and their experiences in one go
                experiences_and_skills_query = """
                        SELECT e.*, s.*, e.name AS exp_name, s.name AS skill_name
                        FROM experiences e
                        LEFT JOIN skills s ON e.exp_id = s.exp_id
                        WHERE e.pos_id = %s
                    """
                experiences_and_skills = self.query(experiences_and_skills_query, (pos_id,))

                for exp_row in experiences_and_skills:
                    exp_id = exp_row['exp_id']

                    if exp_id not in resume_data[inst_id]['positions'][pos_id]['experiences']:
                        resume_data[inst_id]['positions'][pos_id]['experiences'][exp_id] = {
                            'description': exp_row['description'],
                            'end_date': exp_row['end_date'],
                            'hyperlink': exp_row['hyperlink'],
                            'name': exp_row['exp_name'],
                            'skills': {},
                            'start_date': exp_row['start_date']
                        }

                    if exp_row['skill_id']:
                        skill_id = exp_row['skill_id']
                        resume_data[inst_id]['positions'][pos_id]['experiences'][exp_id]['skills'][skill_id] = {
                            'name': exp_row['skill_name'],
                            'skill_level': exp_row['skill_level']
                        }
        print(f"Obtained resume information:\n{resume_data}")
        return resume_data
        # {1: {'address' : 'NULL',
        #                 'city': 'East Lansing',
        #                'state': 'Michigan',
        #                 'type': 'Academia',
        #                  'zip': 'NULL',
        #           'department': 'Computer Science',
        #                 'name': 'Michigan State University',
        #            'positions': {1: {'end_date'        : None,
        #                              'responsibilities': 'Teach classes; mostly NLP and Web design.',
        #                              'start_date'      : datetime.date(2020, 1, 1),
        #                              'title'           : 'Instructor',
        #                              'experiences': {1: {'description' : 'Taught an introductory course ... ',
        #                                                     'end_date' : None,
        #                                                    'hyperlink' : 'https://gitlab.msu.edu',
        #                                                         'name' : 'CSE 477',
        #                                                       'skills' : {},
        #                                                   'start_date' : None
        #                                                 },
        #                                              2: {'description' : 'introduction to NLP ...',
        #                                                     'end_date' : None,
        #                                                     'hyperlink': 'NULL',
        #                                                     'name'     : 'CSE 847',
        #                                                     'skills': {1: {'name'        : 'Javascript',
        #                                                                    'skill_level' : 7},
        #                                                                2: {'name'        : 'Python',
        #                                                                    'skill_level' : 10},
        #                                                                3: {'name'        : 'HTML',
        #                                                                    'skill_level' : 9},
        #                                                                4: {'name'        : 'CSS',
        #                                                                    'skill_level' : 5}},
        #                                                     'start_date': None
        #                                                 }
        #                                             }}}}}
