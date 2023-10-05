from fastapi import FastAPI, APIRouter
from datetime import date


app = FastAPI(
    title="tspycher API",
    description="api's for my Life",
    root_path="/api",
)
router = APIRouter(
    prefix="/api",
    tags=["Api"],
    responses={404: {"description": "Not found"}}
)

from tspycher.api import airfield_router, teltonika_router
from tspycher.api.models import Person


@router.get("/", response_model=Person)
def helo():
    son = Person(birthdate=date(2020, 7, 3))
    daughter = Person(birthdate=date(2022, 7, 11))

    p = Person(
        firstname="Thomas",
        lastname="Spycher",
        nickname="Tom",
        image="https://tspycher.com/img/ai.jpg",
        birthdate=date(1984, 5, 31),
        email="me@tspycher.com",
        instagram="https://www.instagram.com/tspycher/",
        linkedin="https://www.linkedin.com/in/tspycher/",
        website="https://tspycher.com",
        twitter="https://twitter.com/tspycher"
    )
    p.bio = f"Proud Father of a Son ({son.age} years old) and a Daughter ({daughter.age} years old), {p.age} years old, happily married, enthusiastic about cars and planes, IT geek, retired crossfitter (now fat again), beer"
    return p


router.include_router(airfield_router)
router.include_router(teltonika_router)
app.include_router(router)