import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import hashlib
import datetime
import os
import time
import cryptography
from cryptography.fernet import Fernet
from math import pow
import scrypt


class database:

    def __init__(self, bc):

        # Grab information from the configuration file
        self.database = 'db'
        self.host = '127.0.0.1'
        self.user = 'master'
        self.port = 3306
        self.password = 'master'
        self.encryption = {'oneway': {'salt': b'averysaltysailortookalongwalkoffashortbridge',
                                      'n': int(pow(2, 5)),
                                      'r': 9,
                                      'p': 1
                                      },
                           'reversible': {'key': '7pK_fnSKIjZKuv_Gwc--sZEMKn2zc8VvD6zS96XcNHE='}
                           }

    def query(self, query="SELECT CURDATE()", parameters=None):

        cnx = mysql.connector.connect(host=self.host,
                                      user=self.user,
                                      password=self.password,
                                      port=self.port,
                                      database=self.database,
                                      charset='latin1'
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

    def createTables(self, purge=False, data_path='flask_app/database/'):

        table_creation_order = ['institutions.sql', 'positions.sql', 'experiences.sql', 'skills.sql']
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

            for table in os.listdir(data_path + 'create_tables/'):
                if table not in table_creation_order:
                    table_name = os.path.splitext(table)[0]
                    self.query(f"DROP TABLE IF EXISTS {table_name}")

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

    def insertRows(self, table='table', columns=['x', 'y'], parameters=[['v11', 'v12'], ['v21', 'v22']]):
        for parameter in parameters:
            query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in parameter])})"
            self.query(query, parameter)
        print(f"Inserted into table {table}.")

    def createUser(self, email, password, role='user'):
        # Check if email already exists
        existing_user = self.query("SELECT * FROM users WHERE email = %s", (email,))
        if existing_user:
            return {'success': False, 'message': 'Email already exists'}

        # Encrypt password with Bcrypt
        encrypted_password = self.onewayEncrypt(password)

        # Add user to database
        self.query("INSERT INTO users (email, password, role) VALUES (%s, %s, %s)", (email, encrypted_password, role))
        return {'success': True, 'message': 'User created successfully'}

    def authenticate(self, email, password):
        user = self.query("SELECT * FROM users WHERE email = %s", (email,))
        if user and scrypt.hash(password,
                                self.encryption['oneway']['salt'],
                                self.encryption['oneway']['n'],
                                self.encryption['oneway']['r'],
                                self.encryption['oneway']['p']) == user['password']:
            return {'success': True, 'message': 'Authentication successful'}
        else:
            return {'success': False, 'message': 'Invalid email or password'}

    def onewayEncrypt(self, string):
        encrypted_string = hashlib.scrypt(string.encode('utf-8'),
                                          salt=self.encryption['oneway']['salt'],
                                          n=self.encryption['oneway']['n'],
                                          r=self.encryption['oneway']['r'],
                                          p=self.encryption['oneway']['p']
                                          ).hex()
        return encrypted_string

    def reversibleEncrypt(self, type, message):
        fernet = Fernet(self.encryption['reversible']['key'])

        if type == 'encrypt':
            message = fernet.encrypt(message.encode())
        elif type == 'decrypt':
            message = fernet.decrypt(message).decode()

        return message

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
