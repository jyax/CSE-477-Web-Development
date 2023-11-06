# [Web Application Development](https://gitlab.msu.edu/cse477-fall-2023/course-materials/): Homework 2



## Purpose

The purpose of this assignment is to provide you with hands-on experience with backend development including:

1. [Python Flask](https://flask.palletsprojects.com/en/2.0.x/) - a backend for your web application.
2. [MySQL](https://www.mysql.com/) - a relational database to store and retrieve data for your application.
3.  [Jinja](https://jinja.palletsprojects.com/en/3.0.x/) - a tools for generating dynamic HTML content.



## Before you begin

To help you grasp the overarching goal and requirements more concretely, [see the Homework overview video](https://youtu.be/VGlTVNcUJX4). Before you begin this assignment, please complete the following steps.



##### 1. Update your local copy of the Course Materials Repository

Navigate to the <u>course materials repository</u> on your local machine, and pull any updates by running the following command from the terminal:

```bash
git pull https://gitlab.msu.edu/cse477-fall-2023/course-materials.git
```



##### 2. Compose the Homework container locally 

1. Navigate to the `Homework-2` directory of your <u>Personal Course Repository</u> (that's the one with the same name as your netID). 

2. Use `docker-compose` to host the web application locally by executing the following command from you terminal:

   ```bash
   docker-compose -f docker-compose.yml -p hw2-container up
   ```

3. Visit [http://0.0.0.0:8080](http://0.0.0.0:8080) to ensure the template is running.

3. Note that the Homework 2 [Dockerfile](Dockerfile-dev) will install and configure a MySQL 8.0 relational data on the container hosting your web application; you shouldn't need to configure the database.



##### 3. Explore the Template subdirectories

In this assignment, you will modify and extend the web application you developed in Homework 1.  As in Homework 1, we have provided a template app for this assignment in `Homework-2/flask-app/` that you can use to scaffold your assignment. Below we provide an overview of the important directories in this template, with specific call outs to some pre-populated files:

* **`routes.py`**: contains a set of [routes](https://flask.palletsprojects.com/en/2.0.x/api/#flask.Flask.route) that map between specific URLs serviced by your web application (i.e. the location in each `@app.route(<location>)` decorator) to the particular function performed by your web application (i.e. function `def` under each `@app.route`). Some routes have been pre-populated to help you get started; we detail those below:

  * `@app.route('/')`: controls the behavior of the website when a user visits the root directory; in this case, we redirect the user to the `/home` route.

  * `@app.route('/home')`:  renders my html template `home.html	` and passes in a randomly drawn fun fact.

  * `@app.route('/resume')`: extracts `resume_data` from the database, and renders that data within the `resume.html` template.

    

* **`templates/`** : contains a set of `.html` *templates*; templates are distinguished from regular old html files because they can be dynamically populated using [Jinja](https://jinja.palletsprojects.com/en/3.0.x/) (that's the stuff that looks like this `{% ... %}`).  Some templates have been pre-populated to help you get started; we detail those below:

  * `shared/layout.html`: contains an example template that can be extended by other pages in your web application using [Jinja's extends functionality](https://svn.python.org/projects/external/Jinja-1.1/docs/build/inheritance.html).
  * `resume.html` and `home.html`: both extend `template.html`.

  Given that this assignment extends Homework 1, we encourage you to copy over any relevant template files from the previous homework into this assignment directory. 

  

* **`static`** : contains a set of `.css`, `.js` and other static files that your webpage will serve; there is one subdirectory for each page on your website; given that this assignment extends Homework 1, we encourage you to copy over any relevant static files from the previous homework into this assignment directory. 

  

* **`database/create_tables`** : contains a set of `.sql` files; each file specifies a table in your application's database.  Some of the files have been pre-populated to help you get started; we detail those below:

  * `institutions.sql`: contains the `CREATE TABLE` statement for the  `institutions` table which describes all the institutions you've been affiliated with.

  * `positions.sql`: contains the `CREATE TABLE` statement for the `positions` table, which describes all the positions you've held at institutions in the `institutions` tables ; note that the `positions` table has a foreign key (`inst_id`) that references the `institutions` table's primary key. 

    

* **`database/initial_data`** : contains a set of `.csv` files; each file should contain the data used to initially populate a table in your application's database. Some of the files have been pre-populated to help you get started; we detail those below:

  * `institutions.csv`: contains sample data that can be stored in the `institutions` table.
  * `positions.csv`: contains sample data that can be stored in the `positions` table.

  

* **`utils/database/database.py`**:  contains a database python class that takes care of connecting to the database, running queries, and interfacing with Python. Some components of the database utility have already been pre-configured to help you get started; we detail those below:

  * `def __init__`: contains the information needed to connect to the database including the `host`, `user`, `port` and `password`.

  * `def query`:  connects to the database, and executes a query string. You can use the query method in Python by simply passing in a string of the SQL statement you want to execute in the database; for instance:

    ````Python
    from .utils.database.database  import database
    db = database()
    db.query("""SELECT CURDATE()""")
    
    >> [{'CURDATE()': datetime.date(2022, 2, 18)}]
    ````

    Alternatively, you can pass in a string with parameters; this is often useful when inserting into the database, especially when you need to use special characters in the insert statement; for instance:

    ```python
    from .utils.database.database  import database
    db = database()
    db.query("""SELECT * FROM skills where name=%s""", parameters=['HTML'])
    
    >> [{'skill_id': 3, 'experience_id': 2, 'name': 'HTML', 'skill_level': 9}]
    ```

  * `def about`: queries the [information_schema](https://dev.mysql.com/doc/refman/8.0/en/information-schema.html) and returns an overview of your database tables, columns, and keys. results can be returned nested or flat using the boolean `nested` parameter. You don't necessarily have to use this function for the assignment, but I included it in case it's helpful.



## Assignment Goals

Your high-level goal in this assignment is to extend your professional webpage from Homework 1 to include:

1. **A Database**:  allowing you to store persistent information used by your web application.
1. **A Resume page**: providing a HTML version of your Resume (rather than a .pdf). 
2. **A Feedback form**:  Allowing visitors to provide feedback anywhere on your web application.

Your implementation should satisfy both the General Requirements, and Specific Requirements detailed in the sections below. Please note; your implementation does not have to look identical to the example solution. As long as you achieve the Specific and General requirement below, your assignment is complete.



## General Requirements

As a general requirement, we would like you to follow good programming practice, this includes (but is not limited to):

* All code should be commented, organized, and thoughtfully structured.
* Don't mix `HTML`, `CSS`, and `Javascript` in single files.
* `SQL` tables should use foreign keys when appropriate, and contain comments at both the row, and the table level.

Please see the General Requirements section of the [assignment rubric](documentation/rubric.md) for other elements of good programming practice that we'd like you you to pay attention to.



## Specific Requirements

For each of the three assignment goals listed above, we provide a section that outlines the specific requirements associated with that goal, below: 



#### 1. Database requirements

For this portion of the assignment, you will specify a database that allows you to store information used by your web application. This will involve three tasks:  

1. **Specify several database tables** by adding `.sql` files to `database/create_tables` folder; more specifically you will create:

   * **`experiences.sql`**: contains the `CREATE TABLE` statement for the `experiences` table, which describes all the experiences you had at each position in the `positions` table ; the table should contain the following columns:

     * `experience_id`: the primary key, and unique identifier for each experience
     * `position_id`: a foreign key that references  `positions.position_id` 
     * `name`: the name of the experience.
     * `description`: a description of the experience.
     * `hyperlink`: a link where people can learn more about the experience.
     * `start_date`: the state date of the experience.
     * `end_date`: the end date of the experience.

   * **`skills.sql`**: contains the `CREATE TABLE` statement for the `skills` table, which describes all skills associated with each of the experiences in the `experiences` table ; the table should contain the following columns:

     * `skill_id`:  the primary key, and unique identifier for each skill
     * `experience_id`: a foreign key that references  `experiences.experience_id` 
     * `name`: the name of the skill
     * `skill_level`: the level of the skill; 1 being worst, 10 being best.

   * **`feedback.sql`**: contains the `CREATE TABLE` statement for the `feedback` table, which contains user feedback about your website; the table should contain the following columns:

     * `comment_id`: the primary key, and unique identifier for each comment.

     * `name`: the commentators name

     * `email`:  the commentators email

     * `comment`:  The text of the comment

       

2. **Specify the initial data that will populate your tables** by adding `.csv` files to `database/initial_data`; more specifically, you will create (or update):

   1. **`institutions.csv`**: contains data that will be ported into the `institutions` table on initialization of the app.

   2. **`positions.csv`**: contains data that will be ported into the `positions` table on initialization of the app.

   3. **`experiences.csv`**: contains data that will be ported into the `experiences` table on initialization of the app.

   4. **`skills.csv`**:  contains data that will be ported into the `skills` table on initialization of the app.

      

3. **Extend the [database utility](flask_app/utils/database/database.py)** by adding functions that create tables, insert data, and fetch resume data; more specifically, you will populate the following empty function in the database utility:

   1. **`createTables()`**: should create all tables in your database by executing each of the  `.sql` files in `database/create_tables`, and populating them with the initial data provided in `database/initial_data`. Note that `createTables()` is called in `__init__.py` and will therefore be executed upon creation of your application.

   2. **`insertRows()`**: should insert rows into a given table; more specifically, the function should take the table name, a list of column names, and a list of parameter lists (i.e. a list of lists) and execute the appropriate `INSERT` query.

   3. **`getResumeData()`**: should return a nested `dict` that hierarchically represents the complete data  contained in the `institutions`, `positions`, `experiences`, and `skills` tables. Tables should be nested according to their foreign key dependencies. Here's an example of what the the returned data should look like:

      ```json
      {1: {'address': 'NULL',
              'city': 'East Lansing',      
             'state': 'Michigan',
              'type': 'Academia',
               'zip': 'NULL',
        'department': 'Computer Science',
              'name': 'Michigan State University',
         'positions': {1: {'end_date'        : None,
                           'responsibilities': 'Teach classes; mostly NLP and Web design.',
                           'start_date'      : datetime.date(2020, 1, 1),
                           'title'           : 'Instructor',
                           'experiences': {1: {'description' : 'Taught an introductory course ... ',
                                                  'end_date' : None,
                                                 'hyperlink' : 'https://gitlab.msu.edu',
                                                      'name' : 'CSE 477',
                                                    'skills' : {},
                                                'start_date' : None
                                              },
                                           2: {'description' : 'introduction to NLP ...',
                                                  'end_date' : None,
                                                  'hyperlink': 'NULL',
                                                  'name'     : 'CSE 847',
                                                  'skills': {1: {'name'        : 'Javascript',
                                                                 'skill_level' : 7},
                                                             2: {'name'        : 'Python',
                                                                 'skill_level' : 10},
                                                             3: {'name'        : 'HTML',
                                                                 'skill_level' : 9},
                                                             4: {'name'        : 'CSS',
                                                                 'skill_level' : 5}},
                                                  'start_date': None
                                              }
                                          }
                          }
                      }
          }
      }
      ```

      

#### 2. Resume page requirements

For this portion of the assignment, you will write code that generates a dynamic HTML version of your Resume. This will involve two tasks:  

1. **Complete the `resume.html` template** by adding html and jinja statements that dynamically transform the data returned by `getResumeData()` into a dynamic, and <u>mobile friendly</u> resume page; more specifically, your resume page should:
   * <u>For each institution</u>, display:
     * `name` of the institution; this should be left justified.
     * location information for the institution (`department`,`address`, `city` etc.); this should be right justified. 
     * <u>For each affiliated position,</u> display:
       * `title`; this should be left justified
       * `start_date` and `end_date`; this should be right justified.
       * `responsibilities` of the position.
       * <u>For each affiliated experience,</u> display: 
         * `name` of the experience; this should be a hyperlink if the `hyperlink` field is not NULL.
         * `description` of the experience
         * <u>For each affiliated skill, display</u>:
           * `name` of the skill. 
2. **Be mindful of your styling**; while I have not specified specific constraints on the styling here, the content should:
* Look good on both mobile and desktop screens.
  
* Only display a field if it is not `"NULL"` or `None`
  
* Denote the hierarchical relationships in the source data using font-sizes, colors, bullets, etc.



#### 3. Feedback form requirements

For this portion of the assignment, you will generate a feedback form that allows users to send feedback on your site from anywhere in your web application; this will involve three  tasks:

1. **Add an html feedback form** to the `layout.html` template (along with any supporting CSS and JavaScript). The form should contain:

   *  `action` attribute that sends the data to the `/processfeedback` route in `routes.py`.
   *  `method`, and `enctype` attributes that specify a [POST request](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST).
   * The form should contain four `<input>` elements:
     * `name`: a text field that captures the name.
     * `email`: a text field that captures the email.
     * `comment`:  a text field that captures the comment.
     * `submit`: a button that submits the form.
   * The form should be styled such that:
     * the `position` of the form centers it in the screen, even as a user scrolls up or down.
     * the `display` of the form makes it initially invisible.

2. **Add a button that toggles the visibility of the feedback form** to the `layout.html` template. More specifically;

   * When the button is pressed the form should become visible.

   * The button to toggle the feedback form should show up on every page of your application and should always be visible.

3. **Process and store the feedback:**

   * In `routes.py`,  add a route and function to handle the feedback data submitted by the users. Within the route, access the submitted data via `request.form`. It should look something like this:

     ```python
     @app.route('/processfeedback', methods = ['POST'])
     def processfeedback():
     	feedback = request.form
     ```

   * within the `/processfeedback` route, add code that:

     * Inserts the form data into the `feedback` table within the database.

     * Extract all feedback from the `feedback` table
     * Render a template `processfeedback.html` that transform the feedback data into a dynamic, and <u>mobile friendly</u> feedback page; 

     

#### 4. OPTIONAL: Create a Favicon for your website

Visit [this website](https://favicon.io/logo-generator/) to quickly generate a favicon for your site. Add this line to your HTML head; note that the value of the `href` attribute should be the location of the favicon, which may differ from what I'm showing below.

```HTML
<link rel="shortcut icon" href="static/main/images/favicon.ico">
```



## Submitting your assignment

##### Submit Homework 2 Code

1. Submit your assignment by navigating to the main directory of your <u>Personal Course Repository</u> and Pushing your repo to Gitlab; you can do this by running the following commands:

   ```bash
   git add .
   git commit -m 'submitting Homework 2'
   git push
   ```

2. You have now submitted Homework 2's code; you can run the same commands to re-submit anytime before the deadline. Please check that your submission was successfully uploaded by navigating to the corresponding directory in Personal Course Repository online.



**Deploy your web application to Google Cloud**

Deploy your Dockerized App to Google Cloud by running the commands below from the Homework-2 directory.

```bash
gcloud builds submit --tag gcr.io/cse477-fall-2023/homework2
gcloud run deploy --image gcr.io/cse477-fall-2023/homework2 --platform managed
```

* When prompted for service name, press enter.
* When prompted for the `region` choose `us-central1`
* When prompted regarding `unauthenticated invocations` choose  `y`

when the application has completed deploying, it will provide provide an output like this:

```bash
Deploying container to Cloud Run service [homework] in project [cse477-fall-2023] region [us-central1]
✓ Deploying new service... Done.                                            
  ✓ Creating Revision...                                                    
  ✓ Routing traffic...                                                      
  ✓ Setting IAM Policy...                                                   
Done.                                                                       
Service [homework] revision [homework-00001-qol] has been deployed and is serving 100 percent of traffic.
Service URL: https://homework-z7tywrhkpa-uc.a.run.app
```

 The last line in the above output is the <u>Service URL</u>; You can visit the <u>Service URL</u> above to see a live version of your web application. 



##### Submit Homework 2 Survey:

[Submit the Service URL for your live web application in this Google Form](https://docs.google.com/forms/d/e/1FAIpQLSfYojwy_Fwki0HDR8aJnLZrrvLIFEmP-en_zkfkoqpMUBbw4A/viewform). 



