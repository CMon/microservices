from Api import API
from flask import Flask
from flask_login import LoginManager
import random,string

def randomAlphanumeric(stringLength=8):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))

class WebApp(object):
    def __init__(self, configFile, database):
        self.__configFile = configFile
        self.__database = database

    def createApp(self):
        app = Flask(__name__)
        app.secret_key = randomAlphanumeric(20)
        login = LoginManager(app)


        api = API(self.__database)

        globalData = GlobalData()

        administration = Administration(self.__grpcChannel, globalData)
        playback = Playback(self.__grpcChannel, administration, globalData)
        notification = Notification(self.__grpcChannel, globalData)

        @login.user_loader
        def load_user(id):
            # add permission loading as soon as we need more than the user is allowed to do all permission
            return User(id)

        @app.route('/login', methods=['GET', 'POST'])
        def login():
            if current_user.is_authenticated:
                return redirect(url_for('index'))

            globalData.setData("current", "login")
            globalData.setData("error", None)
            if request.method == 'POST':
                config = ConfigHelper.loadSettings(self.__configFile)
                if PasswordHelper.checkPassword(config['adminPass'], request.form['password']):
                    login_user(User("admin"))
                    # handle next page on forced (re)login
                    nextPage = request.args.get('next')
                    if not nextPage or url_parse(nextPage).netloc != '':
                        nextPage = url_for('index')
                    return redirect(nextPage)
                else:
                    globalData.setData("error", 'Invalid Password. Please try again.')

            return render_template('login.html', data=globalData.data())

        @app.route('/logout')
        @login_required
        def logout():
            logout_user()
            return redirect(url_for('index'))

        #playback
        app.add_url_rule('/', view_func=playback.index, methods=['GET'])
        app.add_url_rule('/playback', view_func=playback.playback, methods=['GET', 'POST'])
        app.add_url_rule('/volumeDown', view_func=playback.volumeDown, methods=['POST'])
        app.add_url_rule('/volumeUp', view_func=playback.volumeUp, methods=['POST'])
        app.add_url_rule('/toggleMute', view_func=playback.toggleMute, methods=['POST'])

        # Administration
        app.add_url_rule('/registeredCards', view_func=administration.registeredCards, methods=['GET'])
        app.add_url_rule('/administration/addCard', view_func=administration.addCard, methods=['GET', 'POST'])

        return app
