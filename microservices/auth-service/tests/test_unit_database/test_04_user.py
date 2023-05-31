import sys
import os
import pytest
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "auth_service"))
from Database import Database
from JwtHelper import JwtEncryptionData, JWTAlgorithm

class TestDatabaseUser:
    def setUp(self, databaseFile):
        config = {"file": databaseFile}
        self.db = Database(config)
        assert self.db.addApplication("testApp1", "Application in Test", JwtEncryptionData(JWTAlgorithm.HS384, "secret"))
        assert self.db.addPermission("testApp1", "perm1", "permission1")
        assert self.db.addPermission("testApp1", "perm2", "permission2")
        assert self.db.addApplication("testApp2", "Application in Test", JwtEncryptionData(JWTAlgorithm.HS384, "secret"))
        assert self.db.addPermission("testApp2", "perm1", "permission1")
        assert self.db.addPermission("testApp2", "perm2", "permission2")
    
    def tearDown(self, databaseFile):
        self.db.close()

    @pytest.fixture(autouse=True)
    def before_and_after_test(self, databaseFile):
        self.setUp(databaseFile)    
        yield
        self.tearDown(databaseFile)

    def test_createUser(self):
        assert self.db.addUser("testuser", "password", "me@example.com", "Test User")
        c = self.db._getCursor()
        users = c.execute("SELECT * FROM users WHERE login = 'testuser'")
        allUsers = c.fetchall()
        assert len(allUsers) == 1
        assert len(allUsers[0]) == 4
        assert allUsers[0][0] == "testuser"
        assert allUsers[0][1] != "password"
        assert allUsers[0][1] != ""
        assert allUsers[0][2] == "me@example.com"
        assert allUsers[0][3] == "Test User"

    def test_createUser_double(self):
        assert self.db.addUser("testuser2", "password", "me@example.com", "Test User")
        assert self.db.addUser("testuser2", "password", "me@example.com", "Test User") == False

    def test_checkLogin(self):
        assert self.db.addUser("testuser3", "4321", "me@example.com", "Test User")
        assert self.db.checkPassword("testuser3", "4321")
        assert self.db.checkPassword("testuser3", "1234") == False

    def test_getUser(self):
        assert self.db.addUser("testuser4", "password4", "me4@example.com", "Test User 4")
        user = self.db.getUser("testuser4")
        assert user is not None
        assert user["login"] == "testuser4"
        assert user["email"] == "me4@example.com"
        assert user["fullName"] == "Test User 4"
        assert user["permissions"] == {}
        assert "password" not in user

    def test_getUser_with_permission(self):
        assert self.db.addUser("testuser4p", "password4", "me4p@example.com", "Test User 4p")
        assert self.db.addUserPermission("testuser4p", "testApp1", "perm2")
        user = self.db.getUser("testuser4p")
        assert user is not None
        assert user["login"] == "testuser4p"
        assert user["email"] == "me4p@example.com"
        assert user["fullName"] == "Test User 4p"
        assert user["permissions"] == { "testApp1" : ["perm2"] }
        assert "password" not in user

    def test_getUser_notExisting(self): 
        user = self.db.getUser("testuser-nono")
        assert user is None

    def test_getUsers(self):
        assert self.db.addUser("testuser5", "password4", "me4@example.com", "Test User 4")
        assert self.db.addUser("testuser6", "password4", "me4@example.com", "Test User 4")
        users = self.db.getUsers()
        assert users is not None
        assert len(users) >= 2

    def test_removeUser(self):
        assert self.db.addUser("testuser7", "password4", "me4@example.com", "Test User 4")
        assert self.db.removeUser("testuser7")
        c = self.db._getCursor()
        users = c.execute("SELECT * FROM users WHERE login = 'testuser7'")
        assert len(c.fetchall()) == 0
        userPermissions = c.execute("SELECT * FROM userPermissions WHERE login = 'testuser7'")
        assert len(c.fetchall()) == 0

    def test_removeUser_notExist(self):
        assert self.db.removeUser("testuser-nono") == False

    def test_createUserWithOneApplicationMapping(self):
        assert self.db.addUser("testuserapp1", "1234", "me4@example.com", "Test User 4")
        assert self.db.addUserPermission("testuserapp1", "testApp1", "perm2")
        user = self.db.getUser("testuserapp1")
        assert len(user["permissions"]) == 1
        assert "testApp1" in user["permissions"]
        assert "perm2" in user["permissions"]["testApp1"]

    def test_createUserWithTwoApplicationMappings(self):
        assert self.db.addUser("testuserapp1", "1234", "me4@example.com", "Test User 4")
        assert self.db.addUserPermission("testuserapp1", "testApp1", "perm2")
        assert self.db.addUserPermission("testuserapp1", "testApp2", "perm1")
        user = self.db.getUser("testuserapp1")
        assert len(user["permissions"]) == 2
        assert "testApp1" in user["permissions"]
        assert "testApp2" in user["permissions"]
        assert "perm2" in user["permissions"]["testApp1"]
        assert "perm1" in user["permissions"]["testApp2"]

    def test_removeApplication(self):
        assert self.db.addApplication("removeApp", "Application in Test", JwtEncryptionData(JWTAlgorithm.HS384, "secret"))
        assert self.db.addPermission("removeApp", "perm1", "permission1")
        assert self.db.addPermission("removeApp", "perm2", "permission2")
        assert self.db.addUser("testuserremoveapp", "1234", "me4@example.com", "Test User 4")
        assert self.db.addUserPermission("testuserremoveapp", "removeApp", "perm2")
        assert self.db.addUserPermission("testuserremoveapp", "removeApp", "perm1")
        user = self.db.getUser("testuserremoveapp")
        assert len(user["permissions"]) == 1
        assert "removeApp" in user["permissions"]
        assert "perm2" in user["permissions"]["removeApp"]
        assert "perm1" in user["permissions"]["removeApp"]

        assert self.db.removeApplication("removeApp")
        user = self.db.getUser("testuserremoveapp")
        assert len(user["permissions"]) == 0

        c = self.db._getCursor()
        userPerms = c.execute("SELECT * FROM userPermissions WHERE login = 'testuserremoveapp'")
        allUserPerms = c.fetchall()
        assert len(allUserPerms) == 0

        permissions = c.execute("SELECT * FROM permissions WHERE applicationName = 'removeApp'")
        allPermissions = c.fetchall()
        assert len(allPermissions) == 0

