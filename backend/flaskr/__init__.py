import os
from flask import Flask, request, abort, jsonify, session, json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random
from models import setup_db, Question, Category

ITEMS_PER_PAGE = 10

def paginate_items(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * 10
  end = start + 10
  formatted_selection = [item.format() for item in selection]

  if(len(formatted_selection) < start):
      abort(404)

  return formatted_selection[start:end]


def create_app(test_config=None):
  app = Flask(__name__, instance_relative_config=True)
  # Cors app
  setup_db(app)
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  @app.route('/')
  @cross_origin()
  def helloWorld():
      
    return '''<h1>Hello CORS!</h1> Read about my spec at the
    <a href="http://www.w3.org/TR/cors/">W3</a> Or, checkout my documentation
    on <a href="https://github.com/corydolphin/flask-cors">Github</a>'''
  

  # @TODO: 
  # Create an endpoint to handle GET requests 
  # for all available categories.

  @app.route('/categories')
  def retrieve_categories():
    get_categories = Category.query.order_by(Category.id).all()
    categories = {}

    try:

      for category in get_categories:
        categories[category.id] = category.type

      return jsonify({
        'success': True,
        'categories': categories,
        'total_categories': len(categories)
      })

    except:
      abort(422)

  # @TODO: 
  # Create an endpoint to handle GET requests for questions, 
  # including pagination (every 10 questions). 
  # This endpoint should return a list of questions, 
  # number of total questions, current category, categories. @TODO!! Not complete
 
  @app.route('/questions')
  def retrieve_questions():
    questions = Question.query.order_by(Question.id).all()
    categories = Category.query.order_by(Category.id).all()
    
    categories_list = {}
    
    try:

      for category in categories:
        categories_list[category.id] = category.type
      
      return jsonify({
        'questions': paginate_items(request, questions),
        'total_questions': len(questions),
        'categories': categories_list,
        'current_category': None
      })

    except:
      abort(422)
  
  # TEST: At this point, when you start the application
  # you should see questions and categories generated,
  # ten questions per page and pagination at the bottom of the screen for three pages.
  # Clicking on the page numbers should update the questions. 
  
  # @TODO: 
  # Create an endpoint to DELETE question using a question ID. 

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter_by(id=question_id).one_or_none()

    if question is None:
      abort(404)

    try:
      question.delete()

      return jsonify({
        'success': True,
        'deleted_id': question_id
      })

    except:
      abort(422)


  # TEST: When you click the trash icon next to a question, the question will be removed.
  # This removal will persist in the database and when you refresh the page. 

  # @TODO: 
  # Create an endpoint to POST a new question, 
  # which will require the question and answer text, 
  # category, and difficulty score.

  @app.route('/questions/add', methods=['POST'])
  def create_question():
    body = request.get_json()
    questions = Question.query.order_by(Question.id).all()

    try:

      new_question = body.get('question', None)
      new_answer = body.get('answer', None)
      new_difficulty = body.get('difficulty', None)
      new_category = body.get('category', None)
      
      question = Question(question=new_question, answer=new_answer,
                 difficulty=new_difficulty, category=new_category,)
      
      question.insert()

      return jsonify({
        'success': True,
        'question_id': question.id,
        'questions': paginate_items(request, questions),
        'total_questions': len(questions)
      })

    except:
      abort(422)

  # TEST: When you submit a question on the "Add" tab, 
  # the form will clear and the question will appear at the end of the last page
  # of the questions list in the "List" tab.  
  
  # @TODO: 
  # Create a POST endpoint to get questions based on a search term. 
  # It should return any questions for whom the search term 
  # is a substring of the question. 

  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    search_term = request.get_json()['searchTerm']
    questions = Question.query.all()
    question_list = []

    for q in questions:
      if search_term.lower() in q.question.lower():
        question_list.append(q)
    
    f_questions = [q.format() for q in question_list]

    return jsonify({
      'success':True,
      'questions':f_questions,
      'total_questions':len(question_list),
      'current_category':'None'
    })

  # TEST: Search by any phrase. The questions list will update to include 
  # only question that include that string within their question. 
  # Try using the word "title" to start. 

  # @TODO: 
  # Create a GET endpoint to get questions based on category. 
 
  @app.route('/categories/<int:id>/questions')
  def get_questions_by_category(id):
    questions = Question.query.filter_by(category=id).all()
    current_questions = paginate_items(request, questions)

    formatted_questions = [question.format() for question in questions]
    category = Category.query.filter_by(id=id).all()

    if category is None:
      error = 404

    try:
      return jsonify({
        'success':True,
        'questions':current_questions,
        'total_questions':len(formatted_questions),
        'current_category':category[0].type
      })

    except:
      abort(404)

  # TEST: In the "List" tab / main screen, clicking on one of the 
  # categories in the left column will cause only questions of that 
  # category to be shown. 

  # @TODO: 
  # Create a POST endpoint to get questions to play the quiz. 
  # This endpoint should take category and previous question parameters 
  # and return a random questions within the given category, 
  # if provided, and that is not one of the previous questions. 

  @app.route('/play', methods=['POST'])
  def play_quiz():
    previous_questions = request.get_json()['previous_questions']
    quiz_category = request.get_json()['quiz_category']['id']
    questions = None

    if quiz_category is 0:
      questions = Question.query.all()
    else:  
      questions = Question.query.filter_by(category=str(quiz_category))

    current_question = ''

    for q in questions:
      if q.id not in previous_questions:
        current_question = q.format()
        break

    return jsonify({
      'success':True,
      'question':current_question,
    })

  # TEST: In the "Play" tab, after a user selects "All" or a category,
  # one question at a time is displayed, the user is allowed to answer
  # and shown whether they were correct or not. 

  # @TODO: 
  # Create error handlers for all expected errors 
  # including 404 and 422. 

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(405)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 405,
      "message": "method not allowed"
      }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

    
  return app

    