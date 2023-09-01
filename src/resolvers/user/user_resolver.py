import strawberry
import src.models.user_models as user_models
from src.models.user_models import User
import cloudinary.uploader
from src.gql_schema.input_types.user.user_input_type import UserInputType
from src.gql_schema.object_types.user.user_object_type import UserType
from config.database import SessionLocal,engine
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
import os

#Getting Database Session
user_models.Base.metadata.create_all(bind=engine)
def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

db = next(get_db())

cloudinary.config(
    cloud_name='dxpgzquxz',
    api_key='472164831194559',
    api_secret='vARm6CbxsB4gOmv9y4WiTonJna8'
)
#Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password):
    return pwd_context.hash(password)

#Query
@strawberry.type
class Query:
    @strawberry.field
    def get_users(self)->list[UserType]:
        users=db.query(user_models.User).all()
        users_types=[]
        for user in users:
            user_type=UserType(email=user.email,username=user.username,image=user.image_url)
            users_types.append(user_type)
        return users_types


@strawberry.type
class Mutation:
    @strawberry.field
    def create_users(self,user_input:UserInputType)->UserType:
        try:
            # Upload the profile picture to Cloudinary
            public_id = f"profile_pictures/{os.urandom(16).hex()}"
            response = cloudinary.uploader.upload(
                user_input.image.file,
                folder='profile_pictures',
                public_id=public_id,
                overwrite=True,
            )

            # Create a new user
            user = User(
                email=user_input.email,
                username=user_input.username,
                hashed_password=get_password_hash(user_input.password),
                image_url=response['secure_url']
            )

            db.add(user)
            db.commit()
            db.flush()

            # Return the user as UserType
            user_output = UserType(
                email=user.email,
                image=user.image_url,
                username=user.username
            )
            
            return user_output

        except IntegrityError as e:
            # Handle the case where the username is not unique
            db.rollback()  # Roll back the transaction to avoid data inconsistency
            return UserType(
                email=None,
                image=None,
                username=None,
                error_message="Username is already in use. Please choose a different username."
            )
    

schema = strawberry.Schema(query=Query, mutation=Mutation)



