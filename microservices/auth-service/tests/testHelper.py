class WebTestBackendBase(flask_testing.TestCase):
    __settingsFile = None

    def __createTestConfigFile(self):
        self.__settingsFile = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
        config = ConfigHelper.loadSettings(self.__settingsFile.name)
        config["adminPass"] = "$2b$12$NakHZ6/ZPmsAKmw7JBf3W.3x/QP7lJnEC6I1rYEj9lhjUpUOPse9m" # nimda
        ConfigHelper.storeSettings(self.__settingsFile.name, config)
        return self.__settingsFile.name

    def create_app(self):
        self.assertTrue(self.setupServer())
        webApp = WebApp.WebApp(self.__createTestConfigFile())
        app = webApp.createApp()
        app.config['TESTING'] = True
        return app

    def tearDown(self):
        self.tearDownServer()
        if self.__settingsFile is not None:
            self.__settingsFile.close()
            os.remove(self.__settingsFile.name)
