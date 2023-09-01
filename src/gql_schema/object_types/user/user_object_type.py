import strawberry
from typing import Optional
from strawberry.file_uploads import Upload


@strawberry.type
class UserType():
    username:str
    email:str
    image:str
