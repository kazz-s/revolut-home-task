import datetime
import logging

from couchdb import Server
from couchdb.http import ResourceNotFound

from src.exceptions import MissingData
from settings import *

logger = logging.getLogger(__name__)


_server = Server(url=COUCHDB_URL,
                 full_commit=True,
                 session=None)
_server.resource.credentials = COUCHDB_USER, COUCHDB_PASS


def init():
    logger.info("initialize CouchDB.")
    for db in ['_users', '_replicator', USER_DB_NAME]:
        if db not in _server:
            _server.create(db)


def get_or_create_user_db():
    try:
        return _server[USER_DB_NAME]
    except ResourceNotFound:
        init()
        return _server[USER_DB_NAME]


database = get_or_create_user_db()


def set_date_of_birth(username: str, date_of_birth: datetime.date):
    logger.debug("set %s DoB to %s", username, date_of_birth)
    doc = database.get(username) or {'_id': username}
    doc['date_of_birth'] = date_of_birth.isoformat()

    database.save(doc)


def get_date_of_birth(username: str):
    try:
        iso_date = database[username]['date_of_birth']
    except ResourceNotFound:
        raise MissingData("username not found")
    except KeyError:
        raise MissingData("date of birth not set")
    try:
        return datetime.date.fromisoformat(iso_date)
    except ValueError:
        logger.error("invalid data for %s found: %s", username, iso_date)
        raise MissingData("date of birth not set correctly")
