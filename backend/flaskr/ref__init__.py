import os
from flask import Flask, request, abort, jsonify, session, json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  app = Flask(__name__, instance_relative_config=True)
  # Cors app
  setup_db(app, )
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


  def paginate(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * 10
    end = start + 10
    formattedSelection = [item.format() for item in selection]

    if(len(formattedSelection) < start):
        abort(404)

    return formattedSelection[start:end]

  def searchQuestion(request, searchTerm):
    questions = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).all()

    return jsonify({
      'questions': paginate(request, questions),
      'total_questions': len(questions),
      'current_category': None
    })

  def getQuestionsForCategory(categoryId):
    questions = Question.query.order_by(Question.id).all()
    questionsForCategory = []

    for question in questions:
      if question.category == categoryId:
        questionsForCategory.append(question)
    return questionsForCategory

  @app.route('/categories')
  def getCategories():
    categories = Category.query.order_by(Category.id).all()
    categoriesMap = {}

    for category in categories:
      categoriesMap[category.id] = category.type

    return jsonify({
      'categories': categoriesMap
    })
  
  @app.route('/questions')
  def getQuestions():
    questions = Question.query.order_by(Question.id).all()
    categories = Category.query.order_by(Category.id).all()
    categoriesMap = {}
    for category in categories:
      categoriesMap[category.id] = category.type
    return jsonify({
        'questions': paginate(request, questions),
        'total_questions': len(questions),
        'categories': categoriesMap,
        'current_category': None
    })

  @app.route('/questions/<int:questionId>', methods=['DELETE'])
  def deleteQuestion(questionId):
    error = None
    try:
      question = Question.query.get(questionId);

      if question == None:
        error = 404
        abort(404);

      question.delete()
      questions = Question.query.order_by(Question.id).all()

      return jsonify({
          'questions': paginate(request, questions),
          'total_questions': len(questions),
          'deleted': questionId
      })
    except:
      abort(error) if error else abort(422)

  @app.route('/questions', methods=['POST'])
  def createQuestion():
    body = request.get_json()

    searchTerm = body.get('searchTerm', None)
    newQuestion = body.get('question', None)
    newAnswer = body.get('answer', None)
    newDifficulty = body.get('difficulty', None)
    newCategory = body.get('category', None)

    try:
      if searchTerm != None:
        return searchQuestion(request, searchTerm)

      question = Question(question=newQuestion, answer=newAnswer, 
                 category=newCategory, difficulty=newDifficulty)
      question.insert()

      questions = Question.query.order_by(Question.id).all()

      return jsonify({
        'created': question.id,
        'questions': paginate(request, questions),
        'total_questions': len(questions)
      })
    except:
      abort(422)

  @app.route('/categories/<int:categoryId>/questions')
  def getQuestionsByCategory(categoryId):
    error = None
    try:
      category = Category.query.get(categoryId)

      if category == None:
        error = 404
        abort(404)

      questionsForCategory = getQuestionsForCategory(categoryId)
      return jsonify({
        'questions': paginate(request, questionsForCategory),
        'total_questions': len(questionsForCategory),
        'current_category': category.type
      })
    except:
      abort(error) if error else abort(422)

  @app.route('/quizzes', methods=['POST'])
  def play():
    body = request.get_json()

    previousQuestions = body.get('previous_questions', None)
    quizCategory = body.get('quiz_category', None)

    try:
      questionsForCategory = []
      if quizCategory['type'] == 'click':
        questionsForCategory = Question.query.all()
      else:
        questionsForCategory = getQuestionsForCategory(int(quizCategory['id']))

      filteredQuestions = []

      for question in questionsForCategory:
        if question.id not in previousQuestions:
          filteredQuestions.append(question)

      nextQuestion = random.choice(filteredQuestions).format() if filteredQuestions else None

      return jsonify({
        'question': nextQuestion
      })
    except:
      abort(422)

  @app.errorhandler(400)
  def not_found(error):
      return jsonify({
          'success': False,
          'error': 400,
          'message': 'Unprocessable'
      }), 400
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          'success': False,
          'error': 404,
          'message': 'Not Found'
      }), 404

  @app.errorhandler(405)
  def not_found(error):
      return jsonify({
          'success': False,
          'error': 405,
          'message': 'Bad Request'
      }), 405

  @app.errorhandler(422)
  def not_found(error):
      return jsonify({
          'success': False,
          'error': 422,
          'message': 'Unprocessable'
      }), 422

  @app.errorhandler(500)
  def not_found(error):
      return jsonify({
          'success': False,
          'error': 500,
          'message': 'Internal Server Error'
      }), 500
  
  return app
