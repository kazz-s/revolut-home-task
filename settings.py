from os import getenv

COUCHDB_URL = getenv("COUCHDB_URL", "http://127.0.0.1:5984/")
COUCHDB_USER = getenv("COUCHDB_USER", "admin")
COUCHDB_PASS = getenv("COUCHDB_PASS", "kazz")


USER_DB_NAME = getenv("USER_DB_NAME", "users")

