import fastapi
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from mockers import guido, birthday_boy
from src import db
from src.app import app
from src.exceptions import MissingData

app_client = TestClient(app)


def test_set_future_date_of_birth():
    res = app_client.put(url='/hello/tester',
                         json={"dateOfBirth": "2999-01-01"})

    assert res.status_code == fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY


def test_set_invalid_username():
    res = app_client.put(url='/hello/123456',
                         json={"dateOfBirth": "1956-01-31"})

    assert res.status_code == fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY


def test_set_date_of_birth(mocker: MockerFixture):
    set_date_of_birth = mocker.spy(db, 'set_date_of_birth')

    res = app_client.put(url=f'/hello/{guido.username}',
                         json={"dateOfBirth": guido.born_iso})

    set_date_of_birth.assert_called_once_with(guido.username, guido.born_date)
    assert res.status_code == fastapi.status.HTTP_204_NO_CONTENT


def test_greet_user_not_on_birthday(mocker: MockerFixture):
    get_date_of_birth = mocker.patch('src.db.get_date_of_birth')
    get_date_of_birth.return_value = guido.born_date

    res = app_client.get(url=f'/hello/{guido.username}')

    assert res.status_code == fastapi.status.HTTP_200_OK
    assert guido.username in res.json()['message']


def test_greet_user_on_birthday(mocker: MockerFixture):
    get_date_of_birth = mocker.patch('src.db.get_date_of_birth')
    get_date_of_birth.return_value = birthday_boy.born_date

    res = app_client.get(url=f'/hello/{birthday_boy.username}')

    assert res.status_code == fastapi.status.HTTP_200_OK
    assert "Happy birthday!" in res.json()['message']


def test_missing_data_is_handled(mocker: MockerFixture):
    get_date_of_birth = mocker.patch('src.db.get_date_of_birth')
    get_date_of_birth.side_effect = MissingData

    res = app_client.get(url=f'/hello/fake_user')
    assert res.status_code == fastapi.status.HTTP_404_NOT_FOUND
