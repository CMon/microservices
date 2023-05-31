from Database import Database
from JwtHelper import JWTAlgorithm



class DatabaseHelper(object):
    def __init__(self, db : Database):
        self.__db = db
        self.__jwtData = jwtEncryptionData

    def createAuthApplicationAndPermissions(self):
        self.__db.addApplication("authService", )
