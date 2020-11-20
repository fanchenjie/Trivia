import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "triviatest"
        self.database_path = "postgres://{}/{}".format('xiaofan@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
   
        self.new_question = {
            'question':'question1',
            'answer':'answer1',
            'difficulty':1,
            'category':1
        }
        # edit to test serch by term
        self.search_term_with_result = {
            'searchTerm':'question'
        }
        # self.total_questions_with_search_term = 6
        self.search_term_without_result = {
            'searchTerm':'xxxxxxxxxx'
        }
        # edit these to test delete
        # res = self.client().post('/questions', json = self.new_question)
        # id = json.loads(res.data)['question_id']
        self.exist_question_ID_to_delete = 11
        self.non_exist_question_ID_to_delete = 1000
        # edit these to test non_valid page
        self.non_valid_page = 1000
        # edit these to test get question by category
        self.exist_category_ID = 1
        # edit these to test post quiz type and previous question
        self.quiz_type_previous_questions = {
            'quiz_category':{'id':2},
            'previous_questions':[16]
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
    # get questions
    def test_get_paginated_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
        self.assertFalse(data['current_category'])
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page={}'.format(self.non_valid_page))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Not Found')
    # search by term
    def test_search_question_by_searchTerm_with_result(self):
        res = self.client().post('/questions/searchTerm?page=1', json=self.search_term_with_result)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertFalse(data['current_category'])
        self.assertTrue(data['search_term'])
        # self.assertEqual(data['total_questions'], self.total_questions_with_search_term)
    def test_search_question_by_searchTerm_without_result(self):
        res = self.client().post('/questions/searchTerm?page=1', json=self.search_term_without_result)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 0)
        self.assertFalse(data['current_category'])
        self.assertTrue(data['search_term'])
        self.assertEqual(data['total_questions'], 0)
    def test_400_bad_search_post_without_body(self):
        res = self.client().post('/questions/searchTerm')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Bad Request')
    # get questions by category
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/{}/questions'.format(self.exist_category_ID))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        # self.assertTrue(data['current_category'])
        self.assertFalse(data['search_term'])
    def test_404_questions_by_category_beyond_valid_page(self):
        res = self.client().get('/categories/{}/questions?page={}'.format(self.exist_category_ID, self.non_valid_page))
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Not Found')
    # quizzes
    def test_post_quiz_type_previous_questions(self):
        res = self.client().post('/quizzes', json=self.quiz_type_previous_questions)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])
    def test_400_bad_quiz_post_without_body(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Bad Request')
    # post question
    def test_post_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
    def test_400_bad_post_request_without_body(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Bad Request')
    # delete question
    # def test_delete_question_by_id(self):
    #     res = self.client().delete('/questions/{}'.format(self.exist_question_ID_to_delete))
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    def test_404_if_question_does_not_exist(self):
        res = self.client().delete('/questions/{}'.format(self.non_exist_question_ID_to_delete))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Not Found')
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()