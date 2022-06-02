import json  
from flask import Flask, request, make_response, jsonify, abort, render_template
from flask_cors import CORS, cross_origin
import firebase_admin
from firebase_admin import credentials, firestore
import cv2

#remeber to remove key

app = Flask(__name__)

#make a class function file
class User(object):
    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        #should stay constant
        self.EMAIL = email

    @staticmethod
    def from_dict(source):
        return User(source.username, source.password, source.email)

    def to_dict(self):
        return{
            u'Username' : self.username,
            u'Password' : self.password,
            u'Email' : self.EMAIL 
        }

    def __repr__(self):
        return(
            f'User(\
                name={self.username}, \
                password={self.password}, \
                EMAIL={self.EMAIL}\
                )'
        )

    def createUserDocument(self.username, self.password, self.EMAIl):
        user = User(username,email,password)
        createUserDocument(user.username,user.email,user.password)



jade = User(u'jade1905', u'123456', u'jadesanche2005.com')


CORS(app, resources=r'/api/*')

cred = credentials.Certificate("sign-in-mental-health-firebase-adminsdk-hk8d1-4267dcec2f.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Founder L'}), 404)


@app.route('/api/check_user', methods=["GET"])
def get_user():
    input_json = request.get_json(force=True)
    print(input_json)
    user = User(input_json['Username'], input_json['Password'], input_json['Email'])
    user_ref = db.collection(u'User').document(user.username).get().to_dict()
    if user_ref['Email'] == db.collection(u'User').document(user.email) and user_ref['Password'] == db.collection(u'User').document(user.password):
        return{
            "Status" : "Success",
            "User"   : user_ref
        }
    else:
        return {
            "Status" : "Success",
            "User"   : user.to_dict()
        }    





#@app.route('/health_diagnosis')
#def health_diagnosis():
    
     

if __name__ == '__main__':
    app.run()
