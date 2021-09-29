from importlib import reload

import fastapi
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from pytest import raises

from mockers import guido, birthday_boy
from src.db import get_or_create_user_db, set_date_of_birth, get_date_of_birth
from src.app import app
from src.exceptions import MissingData

from couchdb.http import ResourceNotFound
from settings import USER_DB_NAME


def test_init_when_db_missing(mocker: MockerFixture):
    mocker.patch('src.db._server.__getitem__').side_effect = ResourceNotFound

    create = mocker.patch('src.db._server.create')

    with raises(ResourceNotFound):
        get_or_create_user_db()

    create.assert_called_with(USER_DB_NAME)


def test_set_date_of_birth(mocker: MockerFixture):
    mocker.patch('src.db.database.get').return_value = None
    save = mocker.patch('src.db.database.save')

    set_date_of_birth(guido.username, guido.born_date)

    save.assert_called_once_with({
        "_id": guido.username,
        "date_of_birth": guido.born_iso,
    })


def test_get_date_of_birth(mocker: MockerFixture):
    mocker.patch('src.db.database', {
        guido.username: {
            'date_of_birth': guido.born_iso
        }
    })

    assert get_date_of_birth(guido.username) == guido.born_date


def test_get_date_of_birth_no_user(mocker: MockerFixture):
    mocker.patch('src.db.database.__getitem__').side_effect = ResourceNotFound

    with raises(MissingData):
        get_date_of_birth('any')


def test_get_date_of_birth_missing(mocker: MockerFixture):
    mocker.patch('src.db.database', {guido.username: {}})

    with raises(MissingData):
        get_date_of_birth(guido.username)


def test_get_date_of_birth_corrupted(mocker: MockerFixture):
    mocker.patch('src.db.database', {
        guido.username: {
            'date_of_birth': 'Tuesday'
        }
    })

    with raises(MissingData):
        get_date_of_birth(guido.username)
