import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample
    route after completing the TODOs
    '''
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    setup_db(app)
    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''

    @app.errorhandler(400)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not Found"
        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422
    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories')
    def get_categories():
        query = Category.query.all()
        categories = {}
        for q in query:
            categories[q.id] = q.type
        if len(categories) == 0:
            abort(404)
        return jsonify({'success': True, 'categories': categories})
    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen
    for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions')
    def get_questions():
        questions = Question.query.all()
        page = request.args.get('page', 1, type=int)
        start = (page - 1)*10
        end = start + 10
        formatted_questions = [question.format() for question in questions]
        if len(formatted_questions) <= start:
            abort(404)
        query = Category.query.all()
        categories = {}
        for q in query:
            categories[q.id] = q.type
        return jsonify({'success': True,
                        'questions': formatted_questions[start:end],
                        'total_questions': len(formatted_questions),
                        'categories': categories,
                        'current_category': None, 'search_term': None})
    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def question_deletion(question_id):
        question = \
            Question.query.filter(Question.id == question_id).one_or_none()
        if question is None:
            abort(404)
        try:
            question.delete()
            return jsonify({'success': True})
        except:
            abort(422)
    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at
    the end of the last page
    of the questions list in the "List" tab.
    '''
    @app.route('/questions', methods=['POST'])
    def question_submission():
        try:
            body = request.get_json()
            question = request.json['question']
            answer = request.json['answer']
            difficulty = request.json['difficulty']
            category = request.json['category']
        except:
            abort(400)
        try:
            q = Question(question, answer, category, difficulty)
            q.insert()
        except:
            abort(422)
        return jsonify({'success': True,
                        'question_id': q.id,
                        'total_questions': len(Question.query.all())})

    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

    @app.route('/questions/searchTerm', methods=['POST'])
    def get_questions_by_search():
        page = request.args.get('page', 1, type=int)
        start = (page - 1)*10
        end = start + 10
        try:
            search_term = request.json['searchTerm']
        except:
            abort(400)
        search = '%{}%'.format(search_term)
        questions = \
            Question.query.filter(Question.question.ilike(search)).all()
        formatted_questions = [question.format() for question in questions]
        if len(formatted_questions) != 0 and len(formatted_questions) <= start:
            abort(404)
        return jsonify({'success': True,
                        'questions': formatted_questions[start:end],
                        'total_questions': len(formatted_questions),
                        'current_category': None, 'search_term': search_term})
    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        page = request.args.get('page', 1, type=int)
        start = (page - 1)*10
        end = start + 10
        # category = Category.query.filter_by(id=(category_id)).first().type
        questions = Question.query.filter_by(category=category_id).all()
        formatted_questions = [question.format() for question in questions]
        if len(formatted_questions) <= start:
            abort(404)
        return jsonify({'success': True,
                        'questions': formatted_questions[start:end],
                        'total_questions': len(formatted_questions),
                        'current_category': category_id, 'search_term': None})
    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''

    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        try:
            category = request.json['quiz_category']['id']
            pre_questions = request.json['previous_questions']
        except:
            abort(400)
        if category == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(category=category).all()
        # if all questions are in pre_questions, return None
        if len(pre_questions) == len(questions):
            question = None
            return jsonify({'success': True, 'question': question})
        # else return one random question not in pre_questions
        else:
            random_number = random.randint(0, len(questions)-1)
            while(questions[random_number].format()['id'] in pre_questions):
                random_number = random.randint(0, len(questions)-1)
            question = questions[random_number]

        formatted_question = question.format()
        return jsonify({'success': True, 'question': formatted_question})
    return app
