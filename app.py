from flask import Flask, request, make_response, jsonify, Response, render_template
from flask_cors import CORS
from http import cookies as Cookie
from flask_bootstrap import Bootstrap
from AI import detect_faces
from AIMethods import *
from methods import *


camera = cv2.VideoCapture(0)

#remeber to remove key

app = Flask(__name__)

userCookie = Cookie.SimpleCookie()
sessionId = genSessionId()
userCookie["session"] = sessionId
CORS(app, resources=r'/api/*')
userLoggedIn = False



@app.route('/')
def hello_world():
    return render_template('index.html', loggedIn = userLoggedIn)

@app.route('/login')
def loginSignUp():
    return render_template('login.html')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Founder L'}), 404)



def makeUserCookie(user):
    userCookie["username"] = user.username
    userCookie["email"] = user.EMAIL
    global userLoggedIn
    userLoggedIn = True


def deleteUserCookie():
    userCookie["username"] = ""
    userCookie["email"] = ""
    global userLoggedIn
    userLoggedIn = False

@app.route('/testingRoute', methods=['GET','POST'])
def testing():
    if request.method == 'GET':
        return render_template("AIPage.html",result={},loggedIn = userLoggedIn)
    else:
        data = detect_faces(getFrame(camera))
        return data #,loggedIn = userLoggedIn)

@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route("/accountInfo")
def showAccountInfo():
    if not userLoggedIn:
        return render_template('login.html')
    else:
        user = UserL(userCookie['username'],'password',userCookie['email'])


@app.route('/createUser',methods=["POST"])
def make_user():
    input_json = request.get_json(force=True)
    user = UserL(input_json['username'], input_json['password'],input_json['email'])
    user.makeDocument()
    makeUserCookie(user)
    global userLoggedIn
    userLoggedIn = True
    return {
        "Status" : "Success"
    }

@app.route('/logout')
def loggout():
    deleteUserCookie()
    return render_template("index.html",loggedIn = userLoggedIn)

@app.route('/loginUser', methods=["POST"])# gonna turn int the sign/log in page
def get_user():
    input_json = request.get_json(force=True)
    user = User(input_json['username'], input_json['password'],"email")
    user_ref = db.collection(u'Users').document(user.username).get()
    if user_ref.exists:
        user_ref = user_ref.to_dict()
        user.email = user_ref['email']
        if user_ref['password'] == user.password:
            global userLoggedIn
            userLoggedIn = True
            makeUserCookie(user)
            return{
                "Status" : "Success",
                "User"   : user_ref
            }
        else:
            return {
                "Status": "Failure",
                "User": user.to_dict()
            }
    else:
        return {
            "Status" : "Failure",
            "User"   : user.to_dict()
        }    
        

if __name__ == '__main__':
    app.run(debug=True)
