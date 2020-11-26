from app import db, app, jsonify, request
from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.models.expense import Expense, ExpenseSplit
from app.models.user import User

expense_blueprint = Blueprint('expense', __name__)

@expense_blueprint.route('/expense',methods=['POST'])
@jwt_required
def add_expence():
    data = request.get_json();
    new_expense = Expense(description=data['description'], amount=data['amount'], paid_by=data['paid_by'], split_by=data['split_by'], group_id=data['group_id'], expense_date=data['date'])
    db.session.add(new_expense)
    db.session.flush()
    for member in data['members']:
        new_expense_split = ExpenseSplit(expense_id=new_expense.id, user_id=member['id'],amount_for_user=member['amount_for_user'])
        db.session.add(new_expense_split)
    db.session.commit()
    return jsonify({'message': 'Expense added successfully'})

@expense_blueprint.route('/expense/group/<id>', methods=['GET'])
@jwt_required
def get_all_expense_for_group(id):
    expenses = list()
    expenses_result = Expense.query.filter_by(group_id=id).all()
    for expense in expenses_result:
        print(expense.description)
        expenses.append({
            'id': expense.id, 
            'description': expense.description, 
            'amount': expense.amount, 
            'date': expense.expense_date,
        })
    return jsonify(expenses)

@expense_blueprint.route('/expense/<id>', methods=['GET'])
@jwt_required
def get__expense_details(id):
    expense_details = {}
    expense_details['members'] = list()
    expenses_result = db.session.query(Expense, ExpenseSplit, User).filter(ExpenseSplit.expense_id == id).filter(ExpenseSplit.user_id == User.id).all()

    for expense, expense_split, user in expenses_result:
        expense_details['amount'] = expense.amount
        expense_details['description'] = expense.description
        expense_details['date'] = expense.expense_date
        expense_details['id'] = expense.id
        expense_details['members'].append({'name': user.name, 'mobile': user.mobile, 'email': user.email, 'amount_for_user': expense_split.amount_for_user})
    if 'description' in expense_details:
        return jsonify(expense_details)
    return jsonify({'message': 'Expense details not found.'})
