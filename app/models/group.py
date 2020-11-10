from app import db

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50), nullable=False)
    group_type = db.Column(db.String(50), nullable=False)
    icon = db.Column(db.String(50), nullable=False)
    group_members = db.relationship('GroupMembers', lazy='joined')

class GroupMembers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_mobile = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(50), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
