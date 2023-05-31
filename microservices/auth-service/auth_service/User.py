import jwt
import logging

from JwtHelper import JWTAlgorithm

# TODO: when done with this object change the db.getUser and db.getUsers to return this object here

class User(object):
    __permissions = {} # application => set of permissionNames
    __applicationSecrets = {} # 1:1 mappint applicationName => encryptionDetails (private key or secret, depending on the algo)
    def __init__(self, username, eMail, fullName):
        self.__username = username
        self.__eMail = eMail
        self.__fullName = fullName

    def addPermission(self, application, permission):
        if not application in self.__permissions:
            self.__permissions[application] = []
        if not permission in self.__permissions[application]:
            self.__permissions[application].append(permission)

    def addApplicationSecrets(self, application, algo: JWTAlgorithm, privateOrSecrect, public = None):
        self.__applicationSecrets[application] = {"algo": algo, "private": privateOrSecrect, "public": public}

    def generateJWT(self):
        # generate a master jwt
        # then create multiple jwt's for each application one
        # then put each of the application encrypted jwts inside the master jwt
        # do not encrypt the master jwt
        # the master jwt only contains the userdata, loginname, email, fullName
        raise NotImplementedError()

    def _generateApplicationJWT(self, application):
        if application not in self.__applicationSecrets:
            logging.error(f"No encryption details given for: {application}")
            return None
        encryptionDetails = self.__applicationSecrets[application]

        payload = None
        if application in self.__permissions:
            payload = self.__permissions[application]

        return jwt.encode({'permissions': payload}, encryptionDetails["private"], encryptionDetails["algorithm"])
