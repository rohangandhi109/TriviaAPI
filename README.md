# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#)

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## Running the Frontend

From within the `frontend` directory

To run the server, execute:

```bash
npm install
npm start
```

### API Docuementation

The backend runs on the localhost and the URL: http://localhost:5000/
The frontend runs on the localhost and the URL: http://localhost:3000/

### Error

There are 4 error codes:

- 400 - bad request
- 404 - file/resource not found
- 422 - unprocessable
- 500 - server error

The general format of the error returned in the json format is:

```json
{
  "success": "False",
  "error": "error code(400,404,422,500)",
  "message": "some error message"
}
```

### Endpoints

#### GET '/categories'

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.

- URL: `curl http://127.0.0.1:5000/categories`

  ```json
  {
    "categories": {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
    },
    "success": true
  }
  ```

#### GET '/questions'

- Fetches all the questions stored in the database. The questions are paginated containing 10 questions per page.
- Request Arguments: None
- Returns: An object with list that contains success, questions, categories, totalQuestions, currentCategory
- Just 2 questions are show in the example to keep the doucemetation short.
- URL: `curl http://127.0.0.1:5000/questions`
  ```json{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": null,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
    ],
     "success": true,
    "totalQuestions": 19
  }
  ```

#### DELETE '/questions/<int:id>'

- Deletes a question from the database
- Request Arguments: None
- Returns: json object which contain success and message

- URL: `curl http://127.0.0.1:5000/questions/9 -X DELETE`

```json{
  "message": "Question deleted successfully",
  "success": true
}
```

#### POST '/questions'

- creates a new question
- Request Arguments: question object that contains question, answer, difficulty and category
- Return: json object that contains success and message

- URL: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question": "In which royal palace would you find the Hall of Mirrors?", "answer": "The Palace of Versailles", "difficulty": 3, "category": "3" }'`

```json{
  "message": "Question created successfully",
  "success": true
}
```

#### POST '/questions/search'

- Fetches all the questions that contains the search term in them
- Request Arguments: searchTerm
- Return: json object thats contains success, questions, totalQuestions, currentCategory

URL: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "largest"}'`

```json{
  "currentCategory": null,
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    }
  ],
  "success": true,
  "totalQuestions": 1
}
```

#### GET '/categories/<int:id>/questions'

- Fetches all the questions belonginng to the same category
- Request Argumnet: none
- Return : json object that contains success, questions, totalQuestions, currentCategory
- The example shows 2 questions to keep the documentation short

- URL: `curl http://127.0.0.1:5000/categories/1/questions`

```json{
   "currentCategory": 1,
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
    }
  ],
  "success": true,
  "totalQuestions": 4
}
```

#### POST '/quizzes'

- Fetches a random question of any category or a specific category
- Request argument: previous_questions and quiz_category
- Return: json object for a single random question and success

- URL `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [1, 2], "quiz_category": {"type": "History", "id": "4"}}'`

```json{
  "question": {
    "answer": "George Washington Carver",
    "category": 4,
    "difficulty": 2,
    "id": 12,
    "question": "Who invented Peanut Butter?"
  },
  "success": true
}
```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## Authors

- Rohan Gandhi worked on the API and test suite to integrate with the frontend

- Udacity provided the starter files for the project including the frontend
