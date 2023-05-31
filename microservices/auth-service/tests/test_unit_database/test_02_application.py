import sys
import os
import pytest
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "auth_service"))
from Database import Database
from JwtHelper import JwtEncryptionData, JWTAlgorithm

class TestDatabaseApplication:
    def setUp(self, databaseFile):
        config = {"file": databaseFile}
        self.db = Database(config)

    def tearDown(self, databaseFile):
        self.db.close()

    @pytest.fixture(autouse=True)
    def before_and_after_test(self, databaseFile):
        self.setUp(databaseFile)    
        yield
        self.tearDown(databaseFile)

    def __createAppInput(self):
        return [
            {"name": "testApp1_1", "desc": "Application in test 1", "jwtEnc": JwtEncryptionData(JWTAlgorithm.HS384, "secret")},
            {"name": "testApp1_2", "desc": "Application in test 1", "jwtEnc": JwtEncryptionData(JWTAlgorithm.RS384, "secret", "a not working public")},
        ]

    def test_createApplication(self, subtests):
        for test in self.__createAppInput():
            with subtests.test(i=test):
                assert self.db.addApplication(test["name"], test["desc"], test["jwtEnc"])
                c = self.db._getCursor()
                applications = c.execute("SELECT * FROM applications WHERE name = ?", (test["name"],))
                allApps = c.fetchall()
                assert len(allApps) == 1
                assert len(allApps[0]) == 5
                assert allApps[0][0] == test["name"]
                assert allApps[0][1] == test["desc"]
                assert allApps[0][2] == test["jwtEnc"].algorithm.value
                assert allApps[0][3] == test["jwtEnc"].privateOrSecret
                assert allApps[0][4] == test["jwtEnc"].public

    def test_createApplicationDouble(self):
        assert self.db.addApplication("testApp1-create", "desc1", JwtEncryptionData(JWTAlgorithm.HS384, "secret"))
        assert self.db.addApplication("testApp1-create", "desc1", JwtEncryptionData(JWTAlgorithm.HS384, "secret")) == False

    def __getApplicationInput(self):
        return [
            {"name": "testApp2_1", "desc": "Application in test 2", "jwtEnc": JwtEncryptionData(JWTAlgorithm.HS384, "secret")},
            {"name": "testApp2_2", "desc": "Application in test 2", "jwtEnc": JwtEncryptionData(JWTAlgorithm.RS384, "secret", "a not working public")}, 
        ]

    def test_getApplication(self, subtests):
        for test in self.__createAppInput():
            with subtests.test(i=test):
                assert self.db.addApplication(test["name"], test["desc"], test["jwtEnc"])
                app = self.db.getApplication(test["name"])
                assert app is not None
                assert app["name"] == test["name"]
                assert app["description"] == test["desc"]
                assert str(app["jwtEncrytion"]) == str(test["jwtEnc"])

    def test_getApplication_notExisting(self):
        app = self.db.getApplication("testApp2-nono")
        assert app is None

    def test_getApplications(self):
        assert self.db.addApplication("testApp3", "Application in test 3", JwtEncryptionData(JWTAlgorithm.HS384, "secret"))
        assert self.db.addApplication("testApp4", "Application in test 4", JwtEncryptionData(JWTAlgorithm.HS384, "secret"))
        apps = self.db.getApplications()
        assert apps is not None

    def test_removeApplication(self):
        assert self.db.addApplication("testApp-remove", "Application to remove", JwtEncryptionData(JWTAlgorithm.HS384, "secret"))
        assert self.db.applicationExists("testApp-remove")
        assert self.db.removeApplication("testApp-remove")
        assert self.db.applicationExists("testApp-remove") == False

    def test_removeApplication_notExist(self):
        assert self.db.applicationExists("testApp-remove-nono") == False
        assert self.db.removeApplication("testApp-remove") == False
