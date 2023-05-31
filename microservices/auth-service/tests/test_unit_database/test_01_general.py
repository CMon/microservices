import sys
import os
import pytest
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "auth_service"))
from Database import Database

class TestDatabaseGeneral:
    def setUp(self, databaseFile):
        self.dbFilePath = Path("/tmp/test.sqlite3")
        self.dbFilePath.unlink(missing_ok=True)

    def tearDown(self, databaseFile):
        self.dbFilePath.unlink(missing_ok=True)

    @pytest.fixture(autouse=True)
    def before_and_after_test(self, databaseFile):
        self.setUp(databaseFile)    
        yield
        self.tearDown(databaseFile)

    def test_fileDatabase(self):
        config = {"file": "/tmp/test.sqlite3"}
        db = Database(config)
        assert self.dbFilePath.exists()

        c = db._getCursor()
        tables = c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        foundUsers = False
        foundApplications = False
        foundPermissions = False
        foundUserPermissions = False
        for table in tables:
            if table[0] == "users":
                foundUsers = True
            elif table[0] == "applications":
                foundApplications = True
            elif table[0] == "permissions":
                foundPermissions = True
            elif table[0] == "userPermissions":
                foundUserPermissions = True
        assert foundUsers
        assert foundApplications
        assert foundPermissions
        assert foundUserPermissions

    def test_memoryDatabase(self):
        config = {"file": ":memory:"}
        db = Database(config)
        c = db._getCursor()
        tables = c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        foundUsers = False
        foundApplications = False
        foundPermissions = False
        foundUserPermissions = False
        for table in tables:
            if table[0] == "users":
                foundUsers = True
            elif table[0] == "applications":
                foundApplications = True
            elif table[0] == "permissions":
                foundPermissions = True
            elif table[0] == "userPermissions":
                foundUserPermissions = True
        assert foundUsers
        assert foundApplications
        assert foundPermissions
        assert foundUserPermissions
