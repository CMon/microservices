import sqlite3
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from JwtHelper import JwtEncryptionData, JWTAlgorithm

class Database(object):
    def __init__(self, config):
        self.__conn = sqlite3.connect(config["file"]) # if writing tests, call it ":memory:", then it will exist only for the run of the test
        self.__initDatabase()
        self.__ph = PasswordHasher()

    def __initDatabase(self):
        create = """ 
        CREATE TABLE IF NOT EXISTS users (
            login text PRIMARY KEY NOT NULL,
            passwordHash text NOT NULL,
            email text DEFAULT NULL,
            fullName text DEFAULT NULL
        ); 
        CREATE TABLE IF NOT EXISTS applications (
            name text PRIMARY KEY NOT NULL,
            description text NOT NULL,
            jwtAlg text NOT NULL,
            jwtPrivateOrSecret text NOT NULL,
            jwtPublic text DEFAULT NULL
        );
        CREATE TABLE IF NOT EXISTS permissions (
            name text KEY NOT NULL,
            applicationName text NOT NULL,
            description text NOT NULL,
            PRIMARY KEY(name, applicationName),
            FOREIGN KEY(applicationName) REFERENCES applications(name)
        ); 
        CREATE TABLE IF NOT EXISTS userPermissions (
            login text NOT NULL,
            applicationName text NOT NULL,
            permissionName text NOT NULL,
            PRIMARY KEY(login, applicationName, permissionName),
            FOREIGN KEY(login) REFERENCES users(login),
            FOREIGN KEY(applicationName) REFERENCES applications(name),
            FOREIGN KEY(permissionName) REFERENCES permissions(name)
        ); 

        """
        c = self.__conn.cursor()
        c.executescript(create)

    def _getCursor(self):
        return self.__conn.cursor()

    def close(self):
        self.__conn.commit()
        self.__conn.close()

    def checkPassword(self, login, password) -> bool:
        if not self.userExists(login):
            return False
        c = self.__conn.cursor()
        c.execute("SELECT passwordHash FROM users WHERE login = ?", (login,))
        user = c.fetchall()[0]
        try:
            return self.__ph.verify(user[0], password)
        except VerifyMismatchError:
            return False

    def getUsers(self):
        c = self.__conn.cursor()
        users = c.execute("SELECT u.login, u.email, u.fullName, p.applicationName, p.permissionName FROM users u LEFT JOIN userPermissions p ON u.login = p.login")
        retUsers = {}
        for user in users:
            login = user[0]
            if login not in retUsers:
                retUsers[login] = { "login": login, "email": None, "fullName": None, "permissions": {}}
            email = user[1]
            if email is not None and retUsers[login]["email"] is None:
                retUsers[login]["email"] = email
            fullName = user[2]
            if fullName is not None and retUsers[login]["fullName"] is None:
                retUsers[login]["fullName"] = fullName
            app = user[3]
            if app is not None and not app in retUsers[login]["permissions"]:
                retUsers[login]["permissions"][app] = []
            permission = user[4]
            if permission is not None and not permission in retUsers[login]["permissions"][app]:
                retUsers[login]["permissions"][app].append(permission)
        return list(retUsers.values())

    def getApplications(self):
        c = self.__conn.cursor()
        apps = c.execute("SELECT name, description, jwtAlg, jwtPrivateOrSecret, jwtPublic FROM applications")
        retApps = []
        for app in apps:
            retApps.append({"name": app[0],"description": app[1], "jwtEncrytion": JwtEncryptionData(JWTAlgorithm(app[2]), app[3], app[4])})
        return retApps

    def getPermissions(self, applicationName):
        c = self.__conn.cursor()
        perms = c.execute("SELECT name, description FROM permissions WHERE applicationName = ?", (applicationName,))
        retPerms = []
        for perm in perms:
            retPerms.append({"applicationName": applicationName, "name": perm[0], "description": perm[1]})
        return retPerms

    def getUser(self, login):
        if not self.userExists(login):
            return None
        c = self.__conn.cursor()
        userPerms = c.execute("SELECT u.email, u.fullName, p.applicationName, p.permissionName FROM users u LEFT JOIN userPermissions p ON u.login = p.login WHERE u.login = ?", (login,))
        retUser = { "login": login, "email": None, "fullName": None, "permissions": {}}
        for perm in userPerms:
            email = perm[0]
            if email is not None and retUser["email"] is None:
                retUser["email"] = email
            fullName = perm[1]
            if fullName is not None and retUser["fullName"] is None:
                retUser["fullName"] = fullName
            app = perm[2]
            if app is not None and not app in retUser["permissions"]:
                retUser["permissions"][app] = []
            permission = perm[3]
            if permission is not None and not permission in retUser["permissions"][app]:
                retUser["permissions"][app].append(permission)
        return retUser

    def getApplication(self, name):
        if not self.applicationExists(name):
            return None
        c = self.__conn.cursor()
        c.execute("SELECT name, description, jwtAlg, jwtPrivateOrSecret, jwtPublic FROM applications WHERE name = ?", (name,))
        app = c.fetchall()[0]
        return {"name": app[0],"description": app[1], "jwtEncrytion": JwtEncryptionData(JWTAlgorithm(app[2]), app[3], app[4])}

    def addUser(self, login, password, email, fullName):
        if self.userExists(login):
            return False
        c = self.__conn.cursor()
        c.execute("INSERT INTO users(login, passwordHash, email, fullName) VALUES (?,?,?,?)", (login, self.__ph.hash(password), email, fullName))
        self.__conn.commit()
        return True

    def addApplication(self, name, description, jwtEncrytion: JwtEncryptionData):
        if self.applicationExists(name):
            return False
        c = self.__conn.cursor()
        c.execute("INSERT INTO applications(name, description, jwtAlg, jwtPrivateOrSecret, jwtPublic) VALUES (?,?,?,?,?)", (name, description, jwtEncrytion.algorithm.value, jwtEncrytion.privateOrSecret, jwtEncrytion.public))
        self.__conn.commit()
        return True

    def addPermission(self, applicationName, name, description):
        if not self.applicationExists(applicationName):
            return False
        if self.permissionExists(applicationName, name):
            return False
        
        c = self.__conn.cursor()
        c.execute("INSERT INTO permissions(name, applicationName, description) VALUES (?,?,?)", (name, applicationName, description))
        self.__conn.commit()
        return True

    def removeUser(self, login):
        if not self.userExists(login):
            return False
        c = self.__conn.cursor()
        c.execute("DELETE FROM userPermissions WHERE login = ?", (login,))
        c.execute("DELETE FROM users WHERE login = ?", (login,))
        self.__conn.commit()
        return True

    def removeApplication(self, name):
        if not self.applicationExists(name):
            return False
        c = self.__conn.cursor()
        c.execute("DELETE FROM userPermissions WHERE applicationName = ?", (name,))
        c.execute("DELETE FROM permissions WHERE applicationName = ?", (name,))
        c.execute("DELETE FROM applications WHERE name = ?", (name,))
        self.__conn.commit()
        return True

    def removePermission(self, applicationName, name):
        if not self.permissionExists(applicationName, name):
            return False
        c = self.__conn.cursor()
        c.execute("DELETE FROM userPermissions WHERE applicationName = ? AND permissionName = ?", (applicationName, name,))
        c.execute("DELETE FROM permissions WHERE applicationName = ? AND name = ?", (applicationName, name,))
        self.__conn.commit()
        return True

    def addUserPermission(self, login, applicationName, name):
        if not self.applicationExists(applicationName):
            return False
        if not self.permissionExists(applicationName, name):
            return False

        c = self.__conn.cursor()
        c.execute("INSERT OR IGNORE INTO userPermissions(login, applicationName, permissionName) VALUES (?,?,?)", (login, applicationName, name))
        self.__conn.commit()
        return True

    def userExists(self, login):
        c = self.__conn.cursor()
        c.execute("SELECT * FROM users WHERE login = ?", (login,))
        if len(c.fetchall()) > 0:
            return True
        return False

    def applicationExists(self, name):
        c = self.__conn.cursor()
        c.execute("SELECT * FROM applications WHERE name = ?", (name,))
        if len(c.fetchall()) > 0:
            return True
        return False

    def permissionExists(self, applicationName, name):
        c = self.__conn.cursor()
        c.execute("SELECT * FROM permissions WHERE applicationName = ? AND name = ?", (applicationName, name,))
        if len(c.fetchall()) > 0:
            return True
        return False
