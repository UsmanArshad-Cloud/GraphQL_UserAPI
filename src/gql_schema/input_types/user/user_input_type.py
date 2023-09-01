import strawberry
from typing import Optional
from strawberry.file_uploads import Upload


@strawberry.input
class UserInputType():
    username:str
    email:str
    password:str
    image:Optional[Upload]