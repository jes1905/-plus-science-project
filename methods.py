from datetime import date
from random import randint
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("key/sign-in-mental-health-firebase-adminsdk-hk8d1-ea5dda61b3.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def getUser(user):
    userref = db.collection(u'Users').document(user.username).get()
    if userref.exists:
        if userref['email'] == user.EMAIL:
            return True
        else:
            return False
    else:
        return False


# make a class function file
class User(object):
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        # should stay constant
        self.EMAIL = email

    @staticmethod
    def from_dict(source):
        return User(source.username, source.password, source.email)

    # def makeDocument(self):
    #     user_ref = db.collection(u'User')
    #     user_ref = db.document(self.username).set(self.to_dict())
    #     self.isLoggedIn = True
    #     self.hasDocument = True

    def to_dict(self):
        return {
            u'username': self.username,
            u'password': self.password,
            u'email': self.EMAIL
        }

    def __repr__(self):
        return (
            f'User(\
                name={self.username}, \
                password={self.password}, \
                EMAIL={self.EMAIL}\
                )'
        )


class UserL(User):
    def __init__(self, username, password, email):
        super().__init__(username, password, email)
        self.hasDocument = getUser(self)

    def addEmotionData(self, emotionalData):
        day = getFormattedDate()
        key = "UserData." + day
        user_ref = db.collection(u'Users').document(self.username)
        userCheck = user_ref.get().to_dict()

        if not userCheck['UserData'].has_key(day):
            user_ref.update({
                key: [emotionalData]
            })
        else:
            user_ref.update({
                key: firestore.ArrayUnion([emotionalData])
            })

    def makeDocument(self):
        if not getUser(self):
            user_ref = db.collection(u'Users')
            tempDict = self.to_dict()
            tempDict['UserData'] = {}
            user_ref = user_ref.document(self.username).set(tempDict)
            self.hasDocument = True

    def getData(self):
        return db.collection(u'Users').document(self.username).get().to_dict()


def getFormattedDate():
    fmtStr = "Data of day: "
    day = date.today()
    fmtStr += day
    return fmtStr


def getFormattedDateStr(m, d, y):
    fmtStr = "Data of day: "
    day = str(y) + "-" + str(m) + "-" + d
    fmtStr += day
    return fmtStr


def genSessionId():
    sesStr = ""
    for i in range(1, 30):
        sesStr += str(randint(0, randint(10, 20 * i)))
    return sesStr
