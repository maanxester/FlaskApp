
from engine.app import db

group_association = db.Table('association',
                             db.Column('id', db.Integer),
                             db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                             db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
                             db.PrimaryKeyConstraint('user_id', 'group_id', name='pk_user_group'))
