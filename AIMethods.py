import cv2

def gen_frames(camera):
    # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
def getFrame(camera):
        ret, frame = camera.read()
        if ret:
            cv2.imshow('frame',frame)
            return cv2.imencode(".jpeg",frame)[1].tobytes()


