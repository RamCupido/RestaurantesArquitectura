from app.models.db import User
from app.factories.user_factory import UserFactory
from app.dtos.user_dto import UserDTO
from app.extensions import db


class UserService:
    # Usamos la fábrica para convertir entre modelos y DTOs
    factory = UserFactory()

    #Obtiene todos los usuarios que tienen el rol 'customer'
    @staticmethod
    def get_all_customers():
        users = User.query.filter_by(role='customer').all()
        return [UserService.factory.create_dto_from_model(u) for u in users]

    #Obtiene un usuario por su ID
    @staticmethod
    def get_by_id(user_id):
        user = User.query.get(user_id)
        return UserService.factory.create_dto_from_model(user) if user else None

    #Actualiza la información de un usuario a partir de un DTO
    @staticmethod
    def update(user_id, dto: UserDTO) -> bool:
        try:
            user = User.query.get(user_id)
            if not user:
                return False

            # Actualizar campos
            user.username = dto.username
            user.email = dto.email
            user.role = dto.role

            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error al actualizar usuario: {e}")
            return False
    
    #Elimina un usuario por su ID
    @staticmethod
    def delete(user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False
