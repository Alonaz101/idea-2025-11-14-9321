from backend.app import app, db
from flask import request, jsonify
from flask_jwt_extended import jwt_required

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    recipe_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text)

class IngredientSubstitution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_ingredient = db.Column(db.String(120), nullable=False)
    substitute = db.Column(db.String(120), nullable=False)

@app.route('/api/feedback', methods=['POST'])
@jwt_required()
def post_feedback():
    data = request.json
    user_id = get_jwt_identity()
    rating = data.get('rating')
    recipe_id = data.get('recipe_id')
    comment = data.get('comment', '')

    if not rating or not recipe_id:
        return jsonify({'message': 'rating and recipe_id are required'}), 400
    if not (1 <= rating <= 5):
        return jsonify({'message': 'rating must be between 1 and 5'}), 400

    feedback = Feedback(user_id=user_id, recipe_id=recipe_id, rating=rating, comment=comment)
    db.session.add(feedback)
    db.session.commit()
    return jsonify({'message': 'Feedback submitted'}), 201

@app.route('/api/share_recipe', methods=['POST'])
@jwt_required()
def share_recipe():
    # Simplified: just acknowledge share request
    data = request.json
    recipe_id = data.get('recipe_id')
    platform = data.get('platform')
    if not recipe_id or not platform:
        return jsonify({'message': 'recipe_id and platform are required'}), 400
    # Integration to social APIs to be implemented in future
    return jsonify({'message': f'Recipe {recipe_id} shared on {platform}'}), 200

@app.route('/api/ingredient_substitutions', methods=['GET'])
def ingredient_substitutions():
    original = request.args.get('ingredient')
    if not original:
        return jsonify({'message': 'ingredient query param required'}), 400
    substitutions = IngredientSubstitution.query.filter_by(original_ingredient=original).all()
    results = [s.substitute for s in substitutions]
    return jsonify({'substitutions': results}), 200
