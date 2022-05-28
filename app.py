import json  
from flask import Flask, request, make_response, jsonify, abort, render_template
from flask_cors import CORS, cross_origin
import firebase_admin
from firebase_admin import credentials, firestore, db
#import cv2

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

jade = User(u'jade1905', u'123456', u'jadesanche2005.com')

CORS(app, resources=r'/api/*')

cred = credentials.Certificate("sign-in-mental-health-firebase-adminsdk-hk8d1-4267dcec2f.json")
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL' = https://console.firebase.google.com/u/0/project/sign-in-mental-health/firestore/data/~2FUsers~2FUser}
    )
db = firestore.client()

##cred_obj = firebase_admin.credentials.Certificate('sign-in-mental-health-firebase-adminsdk-hk8d1-4267dcec2f.json')
#default_app = firebase_admin.initialize_app(cred_object, {
#	'databaseURL':https://console.firebase.google.com/u/0/project/sign-in-mental-health/firestore/data/~2FUsers~2FUser
#	})

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Founder L'}), 404)

@app.route('/api/check_user', methods=["POST"])
def get_user():
    input_json = request.get_json(force=True)
    print(input_json)
    user = User(input_json['Username'], input_json['Password'], input_json['Email'])
    user_ref = db.collection(u'User').document(user.username).get().to_dict()
    if user_ref['Email'] == user.email and user_ref['Password'] == user.password:
        return{
            "Status" : "Success",
            "User"   : user_ref
        }
    else:
        return {
            "Status" : "Success",
            "User"   : user.to_dict()
        }    


@app.route('api/journal', methods=["GET"])
def journal():
    input_json = request.get_json(force=True)
    

#@app.route('/health_diagnosis')
#def health_diagnosis():
    
     

if __name__ == '__main__':
    app.run()
