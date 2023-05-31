import sys
import os
import pytest
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "auth_service"))
from JwtHelper import JwtEncryptionData, JWTAlgorithm


class TestJwtHelper(object):
    def __encryptionData_input(self):
        return [
            {"algo" : JWTAlgorithm.HS256, "jwtPrivate": "private", "jwtPublic": "public", "throwMessage":"You provided a public part but the given algorithm (HS256) does not use it"},
            {"algo" : JWTAlgorithm.HS384, "jwtPrivate": "private", "jwtPublic": "public", "throwMessage":"You provided a public part but the given algorithm (HS384) does not use it"},
            {"algo" : JWTAlgorithm.HS512, "jwtPrivate": "private", "jwtPublic": "public", "throwMessage":"You provided a public part but the given algorithm (HS512) does not use it"},
            {"algo" : JWTAlgorithm.HS256, "jwtPrivate": "private", "jwtPublic": None,     "throwMessage": None},
            {"algo" : JWTAlgorithm.HS384, "jwtPrivate": "private", "jwtPublic": None,     "throwMessage": None},
            {"algo" : JWTAlgorithm.HS512, "jwtPrivate": "private", "jwtPublic": None,     "throwMessage": None},

            {"algo" : JWTAlgorithm.RS256, "jwtPrivate": "private", "jwtPublic": "public", "throwMessage": None},
            {"algo" : JWTAlgorithm.RS384, "jwtPrivate": "private", "jwtPublic": "public", "throwMessage": None},
            {"algo" : JWTAlgorithm.RS512, "jwtPrivate": "private", "jwtPublic": "public", "throwMessage": None},
            {"algo" : JWTAlgorithm.RS256, "jwtPrivate": "private", "jwtPublic": None,     "throwMessage": "You selected an algorithm (RS256) that needs a public part please provide one"},
            {"algo" : JWTAlgorithm.RS384, "jwtPrivate": "private", "jwtPublic": None,     "throwMessage": "You selected an algorithm (RS384) that needs a public part please provide one"},
            {"algo" : JWTAlgorithm.RS512, "jwtPrivate": "private", "jwtPublic": None,     "throwMessage": "You selected an algorithm (RS512) that needs a public part please provide one"},

            {"algo" : JWTAlgorithm.ES256, "jwtPrivate": "private", "jwtPublic": "public", "throwMessage": None},
            {"algo" : JWTAlgorithm.ES384, "jwtPrivate": "private", "jwtPublic": "public", "throwMessage": None},
            {"algo" : JWTAlgorithm.ES512, "jwtPrivate": "private", "jwtPublic": "public", "throwMessage": None},
            {"algo" : JWTAlgorithm.ES256, "jwtPrivate": "private", "jwtPublic": None,     "throwMessage": "You selected an algorithm (ES256) that needs a public part please provide one"},
            {"algo" : JWTAlgorithm.ES384, "jwtPrivate": "private", "jwtPublic": None,     "throwMessage": "You selected an algorithm (ES384) that needs a public part please provide one"},
            {"algo" : JWTAlgorithm.ES512, "jwtPrivate": "private", "jwtPublic": None,     "throwMessage": "You selected an algorithm (ES512) that needs a public part please provide one"},

            {"algo" : JWTAlgorithm.PS256, "jwtPrivate": "private", "jwtPublic": "public", "throwMessage": None},
            {"algo" : JWTAlgorithm.PS384, "jwtPrivate": "private", "jwtPublic": "public", "throwMessage": None},
            {"algo" : JWTAlgorithm.PS512, "jwtPrivate": "private", "jwtPublic": "public", "throwMessage": None},
            {"algo" : JWTAlgorithm.PS256, "jwtPrivate": "private", "jwtPublic": None,     "throwMessage": "You selected an algorithm (PS256) that needs a public part please provide one"},
            {"algo" : JWTAlgorithm.PS384, "jwtPrivate": "private", "jwtPublic": None,     "throwMessage": "You selected an algorithm (PS384) that needs a public part please provide one"},
            {"algo" : JWTAlgorithm.PS512, "jwtPrivate": "private", "jwtPublic": None,     "throwMessage": "You selected an algorithm (PS512) that needs a public part please provide one"},
        ]

    def test_EncryptionData(self, subtests):
        for test in self.__encryptionData_input():
            with subtests.test(i=test):
                encData = None
                if test["throwMessage"] is not None:
                    with pytest.raises(Exception) as eInfo:
                        encData = JwtEncryptionData(test["algo"], test["jwtPrivate"], test["jwtPublic"])
                    assert str(eInfo.value) == test["throwMessage"]
                else:
                    encData = JwtEncryptionData(test["algo"], test["jwtPrivate"], test["jwtPublic"])

                    assert encData.algorithm == test["algo"]
                    assert encData.privateOrSecret == test["jwtPrivate"]
                    assert encData.public == test["jwtPublic"]
