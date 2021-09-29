from datetime import date

import fastapi
import pydantic
import uvicorn

from src import db
from src.exceptions import MissingData

app = fastapi.FastAPI()


class UserData(pydantic.BaseModel):
    dateOfBirth: date

    @pydantic.validator('dateOfBirth')
    def must_be_before_today(cls, v):
        assert v < date.today(), "must be a date before the today date"
        return v


@app.put('/hello/{username}')
async def set_date_of_birth(
        user_data: UserData,
        username: str = fastapi.Path(..., regex="^[A-Za-z]+$"),
):

    db.set_date_of_birth(username, user_data.dateOfBirth)

    return fastapi.responses.Response(
        status_code=fastapi.status.HTTP_204_NO_CONTENT
    )


@app.get('/hello/{username}')
async def say_hello(
        username: str = fastapi.Path(..., regex="[A-Za-z]+"),
):
    try:
        date_of_birth = db.get_date_of_birth(username)
    except MissingData:
        return fastapi.responses.Response(
            status_code=fastapi.status.HTTP_404_NOT_FOUND
        )

    today = date.today()
    next_birthday = date_of_birth.replace(year=today.year)
    if next_birthday < today:
        next_birthday = date_of_birth.replace(year=today.year+1)

    msg = 'Happy birthday!' if next_birthday == today else \
        f"Your birthday is in {str(next_birthday - today).split(',')[0]}"

    return {'message': f"Hello, {username}! {msg}"}

if __name__ == "__main__":
    uvicorn.run(app)
