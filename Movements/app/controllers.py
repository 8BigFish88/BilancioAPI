from flask import request, jsonify
from flask_restplus import Resource, fields
from app import db, api, app
from app.models import Movement, Budget
import traceback
from datetime import datetime

movements = api.namespace('api/v1.0/movements', description ='CRUD operation for movements')

budgetModel = movements.model('budgetModel', {
    'name' : fields.String(required=True, validate=True)
    }
)

movementModel = movements.model('movementModel', {
    'amount' : fields.Float(required=True, validate=True),
    'date' : fields.DateTime(required=False, validate=True),
    'entry' : fields.Boolean(required=True, validate=True),
    'description' : fields.String(required=False, validate=True)
    }
)

resp = {200: 'Success', 400: 'movement already in db', 400: 'Content not allowed', \
    400: 'Payload too large', 500: 'Server Error'}


@movements.route('/<int:id_user>')
class Budget_Requests(Resource):
    @movements.expect(budgetModel)
    def post(self,id_user):
        """Post a user budget"""
        data = request.get_json()
        budget = Budget(id_user=id_user, name=data.get('name'))
        db.session.add(budget)
        db.session.commit()
        return jsonify(budget.asDict())


@movements.route('/<int:id_user>/<int:id_budget>')
class Movement_Requests(Resource):
    @movements.expect(movementModel)
    def post(self,id_user,id_budget):
        budget = Budget.query.get(id_budget)
        if not budget:
            return 'budget not found', 404
        if id_user != budget.id_user:
            return 'not allow', 406
        data = request.get_json()
        amount = data.get('amount') 
        date = data.get('date')
        entry = data.get('entry')
        description =  data.get('description')
        date = datetime.strptime(date, '%d/%m/%Y')
        movement = Movement(id_budget=id_budget, amount=amount, 
            date=date, entry=entry, description=description)
        if entry:
            budget.amount += amount
        else:
            budget.amount -= amount
        db.session.add(movement)
        db.session.commit()
        return jsonify(movement.asDict())

    def get(self,id_user,id_budget):
        budget = Budget.query.get(id_budget)
        if not budget:
            return 'budget not found', 404
        response={budget.amount : []}
        print(budget.movements[0].asDict())
        for movement in budget.movements:
            response[budget.amount]+= [movement.amount, movement.date, movement.entry, movement.description]
            print(movement.asDict())
        return jsonify(response)