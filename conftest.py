import unittest.mock

import couchdb


def pytest_configure():
    couchdb.Server = unittest.mock.MagicMock()
