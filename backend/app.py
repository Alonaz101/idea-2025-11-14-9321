from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['JWT_SECRET_KEY'] = 'super-secret'
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)

# User model (SCRUM-403)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

# Recipe model
recipe_tags = db.Table('recipe_tags',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('tag', db.String(50), primary_key=True)
)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    difficulty = db.Column(db.String(50))
    prep_time = db.Column(db.Integer)  # minutes
    tags = db.relationship('Tag', secondary=recipe_tags, backref=db.backref('recipes', lazy='dynamic'))

class Tag(db.Model):
    tag = db.Column(db.String(50), primary_key=True)

# Initialize DB
@app.before_first_request
def create_tables():
    db.create_all()

# User registration (SCRUM-403)
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'User exists'}), 400
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201

# User login (SCRUM-403)
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get('username')).first()
    if user and user.check_password(data.get('password')):
        access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=1))
        return jsonify({'access_token': access_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

# Mood-based recommendation engine (SCRUM-402)
MOOD_TAG_MAP = {
    'happy': ['easy', 'dessert'],
    'stressed': ['comfort', 'quick'],
    'adventurous': ['exotic', 'spicy']
}

@app.route('/api/mood', methods=['POST'])
@jwt_required()
def mood_recommend():
    data = request.json
    mood = data.get('mood')
    if not mood:
        return jsonify({'message': 'Mood not provided'}), 400
    tags = MOOD_TAG_MAP.get(mood.lower(), [])
    # Simple recommendation: return recipes tagged matching mood tags
    if not tags:
        return jsonify({'recipes': []}), 200

    recipes = Recipe.query.join(recipe_tags).filter(recipe_tags.c.tag.in_(tags)).distinct().all()
    results = [{'id': r.id, 'title': r.title, 'difficulty': r.difficulty, 'prep_time': r.prep_time} for r in recipes]
    return jsonify({'recipes': results}), 200

# Recipe search and filtering (SCRUM-404)
@app.route('/api/recipes', methods=['GET'])
def recipes():
    mood = request.args.get('mood')
    difficulty = request.args.get('difficulty')
    max_prep_time = request.args.get('prepTime', type=int)
    query = Recipe.query
    if mood:
        tags = MOOD_TAG_MAP.get(mood.lower(), [])
        if tags:
            query = query.join(recipe_tags).filter(recipe_tags.c.tag.in_(tags))
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    if max_prep_time:
        query = query.filter(Recipe.prep_time <= max_prep_time)
    recipes = query.distinct().all()
    results = [{'id': r.id, 'title': r.title, 'difficulty': r.difficulty, 'prep_time': r.prep_time} for r in recipes]
    return jsonify({'recipes': results}), 200

if __name__ == '__main__':
    app.run(debug=True)
