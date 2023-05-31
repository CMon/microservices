import sys
import os
import pytest
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "auth_service"))
from User import User


class TestUserClass(object):
    @pytest.fixture(autouse=True)
    def before_and_after_test(self):
        self.setUp()    
        yield

    def test_basicCreation(self):
        pass

    def test_addApplication(self):
        pass

    def test_addTwoApplication(self):
        pass

    def test_addMultipleApplicationsWithMultiplePermissions(self):
        pass

    # todo: each test checks the jwts at last, basic has the global encryption, one app has the global and the app encryption, two has three...
