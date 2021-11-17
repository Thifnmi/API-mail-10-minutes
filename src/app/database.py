from run import db
# import sys
# sys.path.append("..")


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


class Mail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cookie = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<email %r>' % self.email


db.create_all()
# print(User.username)
