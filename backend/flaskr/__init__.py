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
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/*":{"origins":"*"}})
  setup_db(app)
  
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods','GET,PATCH,POST,DELETE,OPTIONS')
    return response

  @app.errorhandler(500)
  def internal_error(error):
    return jsonify({
      "success":False,
      "error":500,
      "message":"Internal error"
    }),500

  # @app.route('/')
  # def index():
  #   return jsonify({'message':'hello'})




  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
   
    query = Category.query.all()
    categories = []
    for q in query:
      categories.append(q.type)
    
    # categories = Category.query.all()
    # formatted_categories = [category.format() for category in categories]
    # return jsonify({'success': True, 'categories': formatted_categories})
    return jsonify({'success': True, 'categories':categories})


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    questions = Question.query.all()
    page = request.args.get('page', 1, type = int)
    start = (page - 1)*10
    end = start + 10
    formatted_questions = [question.format() for question in questions]

    # categories = Category.query.all()
    # formatted_categories = [category.format() for category in categories]
    query = Category.query.all()
    categories = []
    for q in query:
      categories.append(q.type)
    return jsonify({'success':True, 'questions':formatted_questions[start : end], 'total_questions':len(formatted_questions), 'categories':categories, 'currentCategory':None})
  


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods = ['POST'])
  def question_submission():
     
    try:
      question = request.json['question']
      # print(question)
      answer = request.json['answer']
      difficulty = request.json['difficulty']
      category_id = request.json['category'] + 1
      print(request.json)
      category = Category.query.filter_by(id = category_id).first().type
      q = Question(question, answer, category, difficulty)
      q.insert()
    except:
      # Question.session.rollback()
      abort(500)
    # finally:
    #   Question.session.close()
    return jsonify({'success':'true'})

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
    
    page = request.args.get('page', 1, type = int)
    start = (page - 1)*10
    end = start + 10
    category = Category.query.filter_by(id = (category_id+1)).first().type
    # print(category)
    questions = Question.query.filter_by(category=category).all()
    formatted_questions = [question.format() for question in questions]
    # print({'success':True, 'questions':formatted_questions[start:end], 'total_questions':len(formatted_questions), 'currentCategory':category_id})
    return jsonify({'success':True, 'questions':formatted_questions[start:end], 'total_questions':len(formatted_questions), 'currentCategory':category_id})




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

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    