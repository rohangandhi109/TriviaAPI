import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


# create a mock question
def mock_question():
    question = Question(question='Some question',
                        answer='some answer',
                        difficulty=3,
                        category='2')
    question.insert()
    return question.id


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', 'postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # 1. check if all categories are retrieved
    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])

    # 2. check the paginated questions are retrived correctly
    def test_get_all_questions(self):
        res = self.client().get('/questions')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['categories'])
        self.assertEqual(data['currentCategory'], None)

    # 3. check if error is thrown for out of bound page
    def test_fail_out_of_bound_page(self):
        res = self.client().get('/questions?page={}'.format(100))
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # 4. check if delete works
    def test_delete_question(self):

        mock_question_id = mock_question()

        res = self.client().delete('/questions/{}'.format(mock_question_id))
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Question deleted successfully')

    # 5. check if delete fails for wrong question id
    def test_fail_delete_questionid_not_present(self):
        res = self.client().delete('/questions/{}'.format(12023))
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # 7. check if create question works
    def test_create_question(self):
        mock_question = {
            'question': 'Some question',
            'answer': 'some answer',
            'difficulty': 1,
            'category': '1'
        }

        res = self.client().post('/questions', json=mock_question)
        data = res.get_json()
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Question created successfully')

    # 8. check if create question fails with empty values
    def test_fail_create_question_blank_values(self):
        mock_question = {
            'question': '',
            'answer': '',
            'difficulty': 1,
            'category': ''
        }

        res = self.client().post('/questions', json=mock_question)
        data = res.get_json()
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unproccessable entity')

    # 9 check if search term works
    def test_search_question(self):
        res = self.client().post('/questions/search',
                                 json={'searchTerm': 'what'})
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])

    # 10 check if a invaild search term fails
    def test_fail_search_question_blank(self):
        res = self.client().post('/questions/search', json={'searchTerm': ''})
        data = res.get_json()

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unproccessable entity')

    # 11 check if the function gets all the question of particular category
    def test_get_questions_of_one_category(self):
        res = self.client().get('/categories/{}/questions'.format(1))
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertEqual(data['currentCategory'], 'Science')

    # 12 check if the functions get a invalid category to revtiver all the question
    def test_fail_get_questions_of_invalid_category(self):
        res = self.client().get('/categories/12345/questions')
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        #self.assertEqual(data['message'], 'Resource not ')

    # 13 check if the quizz works
    def test_random_quizz(self):
        data = {
            'previous_questions': [5, 9],
            'quiz_category': {
                'type': 'History',
                'id': 4
            }
        }
        res = self.client().post('/quizzes', json=data)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(data['question']['id'], '5')
        self.assertNotEqual(data['question']['id'], '9')
        self.assertNotEqual(data['question']['id'], '5')
        self.assertNotEqual(data['question']['category'], '4')

    # 14. check if quizz fails without providing data
    def test_no_data_to_play_quiz(self):

        res = self.client().post('/quizzes', json={})
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
