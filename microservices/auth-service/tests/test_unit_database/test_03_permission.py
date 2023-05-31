import sys
import os
import pytest
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "auth_service"))
from Database import Database
from JwtHelper import JwtEncryptionData, JWTAlgorithm

class TestDatabasePermission:
    def setUp(self, databaseFile):
        config = {"file": databaseFile}
        self.db = Database(config)
        assert self.db.addApplication("testApp", "Application for permissions", JwtEncryptionData(JWTAlgorithm.HS384, "secret"))
    
    def tearDown(self, databaseFile):
        self.db.close()

    @pytest.fixture(autouse=True)
    def before_and_after_test(self, databaseFile):
        self.setUp(databaseFile)    
        yield
        self.tearDown(databaseFile)

    def test_createPermission(self):
        assert self.db.addPermission("testApp", "perm1", "permission1")
        c = self.db._getCursor()
        applications = c.execute("SELECT * FROM permissions WHERE name = 'perm1'")
        allApps = c.fetchall()
        assert len(allApps) == 1
        assert len(allApps[0]) == 3
        assert allApps[0][0] == "perm1"
        assert allApps[0][1] == "testApp"
        assert allApps[0][2] == "permission1"

    def test_createPermissionDouble(self):
        assert self.db.addPermission("testApp", "perm2", "permission2")
        assert self.db.addPermission("testApp", "perm2", "permission2") == False

    def test_getPermissions(self):
        assert self.db.addApplication("testApp2", "Application for permissions", JwtEncryptionData(JWTAlgorithm.HS384, "secret"))
        assert self.db.addPermission("testApp2", "perm1", "permission1")
        assert self.db.addPermission("testApp2", "perm2", "permission2")
        perms = self.db.getPermissions("testApp2")
        assert perms is not None
        foundPerm1 = False
        foundPerm2 = False
        for perm in perms:
            assert perm["applicationName"] == "testApp2"
            if perm["name"] == "perm1" and perm["description"] == "permission1":
                foundPerm1 = True
            if perm["name"] == "perm2" and perm["description"] == "permission2":
                foundPerm2 = True
        assert foundPerm1
        assert foundPerm2

    def test_getPermission_notExisting(self):
        perms = self.db.getPermissions("testApp-perms-nono")
        assert len(perms) == 0

    def test_removePermission(self):
        assert self.db.addPermission("testApp", "perm-remove", "permission to remove")
        perms = self.db.getPermissions("testApp")
        contains = False
        for perm in perms:
            if perm["name"] == "perm-remove":
                contains = True
                break
        assert contains
        assert self.db.removePermission("testApp", "perm-remove")

    def test_removePermission_notExist(self):
        assert self.db.removePermission("testApp", "perm-remove-never-there") == False
