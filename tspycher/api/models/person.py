from pydantic import BaseModel
from datetime import date



class Person(BaseModel):
    firstname:str = None
    lastname:str = None
    nickname:str = None
    image:str = None

    birthdate:date = None
    bio:str = None
    email:str = None

    instagram:str = None
    linkedin:str = None
    website:str = None
    twitter:str = None

    @property
    def age(self) -> int:
        today = date.today()
        return today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))

    def dict(self, *args, **kwargs):
        result = super().dict(*args, **kwargs)
        result["age"] = self.age
        return result

    class Config:
        orm_mode = True