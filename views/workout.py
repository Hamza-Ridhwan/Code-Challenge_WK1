from flask import jsonify, request, Blueprint
from models import db, User, Workout
from flask_jwt_extended import jwt_required, get_jwt_identity

workout_bp= Blueprint("workout_bp", __name__)

# Create Workout
@workout_bp.route("/workout/add", methods=["POST"])
@jwt_required()
def add_workout():
    data = request.get_json()
    current_user_id = get_jwt_identity()

    workout_type = data['workout_type']
    duration = data['duration']
    calories_burned = data['calories_burned']

    check_workout = Workout.query.filter_by(workout_type=workout_type).first()

    if check_workout:
        return jsonify({"Error":"Workout already exists"}),406

    else:
        new_workout = Workout(workout_type=workout_type, duration=duration, user_id=current_user_id, calories_burned=calories_burned)
        db.session.add(new_workout)
        db.session.commit()
        return jsonify({"Success":"Workout added successfully"}), 201

    
# Read Workouts
@workout_bp.route('/workouts', methods=['GET'])
@jwt_required()
def get_workouts():
    user_id = get_jwt_identity()
    workouts = Workout.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': w.id, 'workout_type': w.workout_type, 'duration': w.duration, 'calories_burned': w.calories_burned} for w in workouts])


# Update Workout
@workout_bp.route('/workout/update/<int:id>', methods=['PATCH'])
@jwt_required()
def update_workout(id):
    user_id = get_jwt_identity()
    workout = Workout.query.get(id)
    if workout and workout.user_id == user_id:
        data = request.get_json()
        workout.workout_type = data.get('workout_type', workout.workout_type)
        workout.duration = data.get('duration', workout.duration)
        workout.calories_burned = data.get('calories_burned', workout.calories_burned)
        db.session.commit()
        return jsonify({'message': 'Workout updated successfully'})
    return jsonify({'message': 'Workout not found'}), 404

# Delete Workout
@workout_bp.route('/workout/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_workout(id):
    user_id = get_jwt_identity()
    workout = Workout.query.get(id)
    if workout and workout.user_id == user_id:
        db.session.delete(workout)
        db.session.commit()
        return jsonify({'message': 'Workout deleted successfully'})
    return jsonify({'message': 'Workout not found or unauthorized'}), 404