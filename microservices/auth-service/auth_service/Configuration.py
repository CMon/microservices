import yaml

class Configuration(object):
    def __init__(self, configFile):
        self.__configFile = configFile
        self.loadConfig()
    
    def loadConfig(self):
        with open(self.__configFile, 'r') as f:
            self.__configYaml = yaml.safe_load(f)

    def getSection(self, section):
        return self.__configYaml["authService"][section]