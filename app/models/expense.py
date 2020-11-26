from app import db

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    split_by = db.Column(db.String(50), nullable=False)
    expense_date = db.Column(db.String(30), nullable=False)
    paid_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    expense_split = db.relationship('ExpenseSplit', lazy='joined')

class ExpenseSplit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount_for_user = db.Column(db.Integer, nullable=False)