import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def get_pagination(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={'/': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    # get all categories
    # Create an endpoint to handle GET requests
    # for all available categories.
    @app.route('/categories')
    def get_categories():
        selection = Category.query.all()
        category = {}
        for c in selection:
            category[c.id] = c.type

        if len(category) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'categories': category
        }), 200

    # 1. Create an endpoint to handle GET requests for questions,
    # including pagination (every 10 questions).
    # This endpoint should return a list of questions,
    # number of total questions, current category, categories.
    @app.route('/questions')
    def get_questions():
        selection = Category.query.all()
        categories = {}
        for c in selection:
            categories[c.id] = c.type

        if len(categories) == 0:
            abort(404)

        selection = Question.query.all()
        questions = get_pagination(request, selection)
        if len(questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': questions,
            'totalQuestions': len(selection),
            'categories': categories,
            'currentCategory': None
        }), 200

    # 2. Create an endpoint to DELETE question using a question ID.
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            question = Question.query.get(id)
            if question is None:
                abort(404)
            question.delete()
            return jsonify({
                'success': True,
                'message': 'Question deleted successfully'
            }), 200
        except:
            abort(404)

    # 3. Create an endpoint to POST a new question,
    # which will require the question and answer text,
    # category, and difficulty score.
    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            body = request.get_json()
            new_question = body.get('question', '')
            new_answer = body.get('answer', '')
            new_difficulty = body.get('difficulty', '')
            new_category = body.get('category', '')

            new_record = Question(question=new_question, answer=new_answer,
                                  difficulty=new_difficulty, category=new_category)
            new_record.insert()

            return jsonify({
                'success': True,
                'message': 'Question created successfully'
            }), 201
        except:
            abort(422)

    # 4. Create a POST endpoint to get questions based on a search term.
    # It should return any questions for whom the search term
    # is a substring of the question.
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        try:
            body = request.get_json()
            searchTerm = body.get('searchTerm', '')
            if searchTerm == '':
                abort(422)
            selection = Question.query.filter(
                Question.question.ilike(f'%{searchTerm}%')).all()
            questions = get_pagination(request, selection)
            return jsonify({
                'success': True,
                'questions': questions,
                'totalQuestions': len(selection),
                'currentCategory': None
            }), 200
        except:
            abort(422)

    # 5. Create a GET endpoint to get questions based on category.
    @app.route('/categories/<int:id>/questions')
    def get_questions_by_category(id):
        try:
            category = Category.query.get(id)
            if category is None:
                abort(404)
            selection = Question.query.filter_by(category=id).all()
            questions = get_pagination(request, selection)
            if len(questions) == 0:
                abort(404)
            return jsonify({
                'success': True,
                'questions': questions,
                'totalQuestions': len(selection),
                'currentCategory': category.type
            }), 200
        except:
            abort(404)

    # 6. Create a POST endpoint to get questions to play the quiz.
    # This endpoint should take category and previous question parameters
    # and return a random questions within the given category,
    # if provided, and that is not one of the previous questions.
    @app.route('/quizzes', methods=['POST'])
    def play_quizzes():
        try:
            body = request.get_json()
            previous_question = body.get('previous_questions', '')
            quiz_category = body.get('quiz_category', '')

            if (previous_question is None) or (quiz_category is None):
                abort(404)

            if quiz_category['id'] == '0':
                selection = Question.query.all()
            else:
                selection = Question.query.filter_by(
                    category=quiz_category['id']).all()

            new_question = random.choice(selection)

            for uniqueID in previous_question:
                if uniqueID == new_question.id:
                    new_question = random.choice(selection)

            if len(previous_question) == len(selection):
                abort(404)

            return jsonify({
                'success': True,
                'question': new_question.format()
            }), 200

        except:
            abort(404)

    # 422 error

    @ app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unproccessable entity'
        }), 422

    # 404 error
    @ app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    # 500 error
    @ app.errorhandler(500)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Server side error'
        }), 500

    # 405 error
    @ app.errorhandler(405)
    def worng_url(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Wrong method for the url'
        }), 405

    return app
