# The Trivia API Documentation

The Trivia API is a full-stack application that allows users to play a trivia game wthere they can search for questions to answer, post new questions as well as delete the ones they don't like. The aplications backend is built in Python, JS, React and a Posgres databases whe the data is stored, accesed and edited by the application.

## Getting Started

### Project structure

```
├── README.md
├── backend
│   ├── README.md
│   ├── __pycache__
│   ├── flaskr
│   ├── models.py
│   ├── pip
│   ├── requirements.txt
│   ├── test_flaskr.py
│   └── trivia.psql
├── env
│   ├── bin
│   ├── include
│   ├── lib
│   └── pyvenv.cfg
└── frontend
    ├── README.md
    ├── build
    ├── node_modules
    ├── package-lock.json
    ├── package.json
    ├── public
    └── src
````

# API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.
- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```
## Running the server
From within the `backend` directory first ensure you are working using your created virtual environment.
To run the server, execute:
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

# API Frontend

## Getting Setup

> _tip_: this frontend is designed to work with [Flask-based Backend](../backend). It is recommended you stand up the backend first, test using Postman or curl, update the endpoints in the frontend, and then the frontend should integrate smoothly.

### Installing Dependencies: Node and NPM
This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:
```bash
npm install
```
>_tip_: **npm i** is shorthand for **npm install**
Open a terminal in `/frontend` directory and run:
```bash
npm install
```
and then run:
```bash
npm start
```
Open http://localhost:3000 to view the frontend in the browser.

#### Running tests
To set up tests, navigate to the `/backend` directory and run:
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
```
next, change the self.database_path in test_flaskr.py (line 18) to match your PostgreSQL user and password.  
Then you can run tests by running from the `/backend` directory:
```bash
python test_flaskr.py
```
## The API Reference
The following examples list the available endpoints and the expected respomnses from the request commands.

### GET /categories
Returns a list of available categories
`curl http://127.0.0.1:5000/categories -X GET`

    {
      "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
      },
      "success": true,
      "total_categories": 6
    }


### GET /questions
Returns a list of available categories and questions, number of questions, and current category.
`curl http://127.0.0.1:5000/questions -X GET`

    {
        "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
        "current_category": null,
        "questions": [
    {
        "answer": "Apollo 13",
        "category": 5,
        "difficulty": 4,
        "id": 2,
         "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
        "answer": "Tom Cruise",
        "category": 5,
         "difficulty": 4,
         "id": 4,
         "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
    ],
         "total_questions": 22
    }
	
	
### DELETE /questions/<id>
Deletes a question with provided ID.
`curl http://127.0.0.1:5000/questions/50 -X DELETE`

	{
        "deleted_id": 50, 
        "success": true
    }
	    or
	{
        "error": 404, 
        "message": "resource not found", 
         "success": false
    }


### POST /questions/add
Creates a question. 
`curl http://127.0.0.1:5000/questions/add -X POST -H "Content-Type: application/json" -d '{"question":"TestQuestion","answer":"TestAnswer","category":"5","difficulty":"5"}'`
	
	{
        "question_id": 51,
        < a dictionary of current cuestions here >
        "success": true, 
        "total_questions": 19
	}
	    or
	{
        "error": 400, 
        "message": "bad request", 
        "success": false
    }

### POST /questions
Searces questions by search-term. Case insensitive.
Returns a list of questions, the number of questions returned, and current category.
`curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"anne"}'`

	{
        "current_category": "None", 
        "questions": [
    {
        "answer": "Tom Cruise", 
        "category": 5, 
        "difficulty": 4, 
        "id": 4, 
        "question": "What actor did author Anne Rice first denounce, 
                     then praise in the role of her beloved Lestat?"
    }
    ],
        "success": true, 
        "total_questions": 1
     }


### GET /categories/<int:id>/questions
Gets all questions that belong to a specific category.
Returns a list of questions, total number of questions returned, and current category.
`curl http://127.0.0.1:5000/categories/1/questions -X GET`

	{
        "current_category": "Science", 
        "questions": [
    {
        "answer": "The Liver", 
        "category": 1, 
        "difficulty": 4, 
        "id": 20, 
        "question": "What is the heaviest organ in the human body?"
    }, 
    {
        "answer": "Alexander Fleming", 
        "category": 1, 
        "difficulty": 3, 
         "id": 21, 
         "question": "Who discovered penicillin?"
    }, 
    {
         "answer": "Blood", 
         "category": 1, 
         "difficulty": 4, 
         "id": 22, 
         "question": "Hematology is a branch of medicine involving the study of what?"
    }
    ], 
        "success": true, 
        "total_questions": 3
    }
  
## Error Handling
The application will return the following errors:
- 400 Bad Request
- 404 Not found
- 405 Method not allowed
- 422 Unprocessable

All errors are returned as JSON responses and formatted as in the following example:

	{
        "error": 405, 
        "message": "method not allowed", 
        "success": false
    }


