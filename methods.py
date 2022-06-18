from datetime import date, datetime
from random import randint
from math import floor
import cookies
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("key/sign-in-mental-health-firebase-adminsdk-hk8d1-ea5dda61b3.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def getUser(user):
    userref = db.collection(u'Users').document(user.username).get()
    if userref.exists:
        userref = userref.to_dict()
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
        if not 'UserData' in userCheck:
            user_ref.set({'UserData': {}}, merge=True)
        if not day in 'UserData':
            fmtStr = 'UserData.' + day
            user_ref.set({fmtStr: {}}, merge=True)
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

# TODO: Add feature checking the day of the week and formatting all data by
#  Week -> {Monday:[MondayData], Tuesday ..., Sunday: [SundayData]}
# def getDayOfWeek(m, d, y):
#     daysOfTheWeek = ["N/A", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
#     monthKeys = [0, 1, 4, 4, 0, 2, 5, 0, 3, 6, 1, 4, 6]
#     day = int(str(y)[2:])
#     day = floor(day / 4)
#     day += d
#     day += monthKeys[m]
#     if m == 0 or m == 1 and y % 4 == 0 and (y % 100 != 0 or y % 400 and y % 100 == 0):
#         day -= 1
#     topTwo = floor(y / 100)
#     while topTwo < 20:
#         topTwo += 4
#     if (topTwo - 17) % 4 == 0:
#         day += 4
#     elif (topTwo - 18) % 4 == 0:
#         day += 2
#     elif (topTwo - 19) % 4 == 0:
#         day += 0
#     elif (topTwo - 20) % 4 == 0:
#         day += 6
#     day += int(str(y)[2:])
#     day = day % 7
#     return day


def getFormattedDate():
    fmtStr = "Data of day: "
    now = datetime.now()
    # y = now.strftime("%Y")
    # m = now.strftime("%m")
    # d = now.strftime("%d")
    # dayIndex = getDayOfWeek(m,d,y)
    day = datetime.now().strftime("%Y-%m-%d")
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
