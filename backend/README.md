# Full Stack Trivia API Backend

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

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. ✅
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET '/questions'
GET '/categories/<category_id>/questions'
POST '/questions'
POST '/questions/searchTerm'
POST '/quizzes'
DELETE '/questions/<question_id>'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- Fetches a list of questions, number of total questions, current category, categories
- Request Arguments: page
- Returns: An object with keys:
  total_questions, the total number of questions contain the search term.
  categories, contains a object of id: category_string key:value pairs.
{'1' : "Science",
 '2' : "Art"}
  current_category.
  search_term.
  questions, that contains a list of question objects. 
[
{
"answer": "1",
"category": "Science",
"difficulty": 1,
"id": 37,
"question": "1"
},
{
"answer": "2",
"category": "Science",
"difficulty": 2,
"id": 38,
"question": "2"
},
{
"answer": "3",
"category": "Science",
"difficulty": 1,
"id": 39,
"question": "3"
},
{
"answer": "4",
"category": "Science",
"difficulty": 1,
"id": 40,
"question": "4"
},
{
"answer": "5",
"category": "Science",
"difficulty": 1,
"id": 41,
"question": "5"
},
{
"answer": "6",
"category": "Science",
"difficulty": 1,
"id": 42,
"question": "6"
},
{
"answer": "7",
"category": "Science",
"difficulty": 5,
"id": 43,
"question": "7"
},
{
"answer": "8",
"category": "Science",
"difficulty": 1,
"id": 44,
"question": "8"
},
{
"answer": "9",
"category": "Science",
"difficulty": 1,
"id": 45,
"question": "9"
},
{
"answer": "10",
"category": "Science",
"difficulty": 1,
"id": 46,
"question": "10"
}
],

GET '/categories/<category_id>/questions'
- Fetches a list of questions based on category
- Request Arguments: category_id
- Returns: An object with keys: 
  total_questions, the total number of questions contain the search term.
  current_category.
  search_term.
  questions, that contains a list of question objects. 
[
{
"answer": "22",
"category": "Art",
"difficulty": 1,
"id": 48,
"question": "22"
},
{
"answer": "23",
"category": "Art",
"difficulty": 1,
"id": 49,
"question": "23"
},
{
"answer": "24",
"category": "Art",
"difficulty": 1,
"id": 50,
"question": "24"
},
{
"answer": "25",
"category": "Art",
"difficulty": 1,
"id": 59,
"question": "25"
}
]

POST '/questions'
- Create a new question
- Request Arguments: the question and answer text, category, and difficulty score
- Returns: An object with keys, success, total_questions. 

POST '/questions/searchTerm'
- Get questions based on a search term
- Request Arguments: searchTerm
- Returns: An object with keys: 
  total_questions, the total number of questions contain the search term.
  current_category.
  search_term.
  questions, that contains a list of question objects.
[
{
"answer": "3",
"category": "Art",
"difficulty": 1,
"id": 48,
"question": "3"
},
{
"answer": "13",
"category": "Science",
"difficulty": 1,
"id": 58,
"question": "13"
},
{
"answer": "23",
"category": "Art",
"difficulty": 1,
"id": 88,
"question": "23"
}
]

POST '/quizzes'
- Get questions to play the quiz
- Request Arguments: category, previous question parameters
- Returns: An object with a single key, question, that contains a question object.
[
{
"answer": "25",
"category": "Art",
"difficulty": 1,
"id": 59,
"question": "25"
}
]

DELETE '/questions/<question_id>'
- Delete question based on question id
- Request Arguments: question_id
- Returns: An object with a single key, success.

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```