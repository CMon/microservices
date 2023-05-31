from flask import render_template, request
from flask_login import login_required

class API(object):
    def __init__(self, databaseFile):
        pass

    def login(self):
        pass

    @login_required
    def logout(self):
        raise NotImplementedError()

########### User API
    @login_required
    def getUser(self, login):
        raise NotImplementedError()

    @login_required
    def getUsers(self):
        raise NotImplementedError()

    @login_required
    def addUser(self):
        raise NotImplementedError()

    @login_required
    def removeUser(self):
        raise NotImplementedError()

########### Application API
    @login_required
    def getApplication(self, appName):
        raise NotImplementedError()

    @login_required
    def getApplications(self):
        raise NotImplementedError()

    @login_required
    def addApplication(self):
        #TODO: if add application is without a secret it creates one if the algo is using public/private, then create both
        raise NotImplementedError()

    @login_required
    def removeApplication(self, appName):
        raise NotImplementedError()

########### Application - permission API
    @login_required
    def getPermission(self, appName, permName):
        raise NotImplementedError()

    @login_required
    def getPermissions(self, appName):
        raise NotImplementedError()

    @login_required
    def addPermission(self, appName, permName):
        raise NotImplementedError()

    @login_required
    def removePermission(self, appName, permName):
        raise NotImplementedError()
