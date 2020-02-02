from flask_restful import Resource

from werkzeug.security import generate_password_hash

from models import Room, Participant
from models_schemas import room_schema, rooms_schemas, participant_schema

from extensions import db

from utils.validators import check_fields
from utils.auth import token_required


"""
post: create a new room
    *required fileds
    - name (unique)
    - password
"""
class Rooms(Resource):

    def is_room_name_already_in_use(self, name: str) -> bool:
        return Room.query.filter(Room.name == name).first() is not None

    @token_required
    def get(self, **kwargs):
        
        pass

    # create a new room
    @token_required
    @check_fields(fields=("name", "password"))
    def post(self, **kwargs):

        user = kwargs.get('user')
        fields = kwargs.get('fields')

        name = fields.get('name')
        password = generate_password_hash(fields.get('password'))

        if self.is_room_name_already_in_use(name):
            return {'error': 'Already exist a room with this name'}, 400

        room = Room(name, password)
        participant = Participant(user, room)

        try:
            db.session.add(room)
            db.session.add(participant)

            db.session.commit()

            return {
                'message': 'New room successfully created',
                'data': room_schema.dump(room)
            }, 201

        except:
            
            return {'message': 'Internal error'}, 500


"""
get: return a specific room
"""
class GetOneRoom(Resource):

    def get(self, room_id):
        room = Room.query.filter_by(id=room_id).first_or_404("Room id cannot be find")
        return {
            'message': 'Room successfully find',
            'data': room_schema.dump(room)
        }


"""
get: return a list with all rooms
"""
class GetAllRooms(Resource):

    def get(self):
        rooms = Room.query.all()
        return {
            'message': 'Rooms successfully find',
            'data': rooms_schemas.dump(rooms)
        }