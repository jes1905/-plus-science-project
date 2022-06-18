# this code is taken from the Google Vision API Documentation (with a few changes)

def detect_faces(content):
    """Detects faces in an image."""
    from google.cloud import vision
    #Beginning client
    client = vision.ImageAnnotatorClient()


    #sending our image through to be processed by the AI
    image = vision.Image(content=content)

    #getting a response
    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')

    #Setting a res variable in case there are more than one face
    #The formatting is a dict(json) holding an array with the key faces, we intialize it with the number of faces in the response
    #You could replace the res dict with a faces arr with each face as it's own index in the array as a json
    res = {'faces':[0 for i in faces]}
    faceIndex = 0
    for face in faces:

        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))
        #Setting the face's values to the proper index (we send the information in as a dict
        res['faces'][faceIndex] = {
            'anger': likelihood_name[face.anger_likelihood],
            'joy': likelihood_name[face.joy_likelihood],
            'surprise': likelihood_name[face.surprise_likelihood]
        }


    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    print(res)
    print(len(res))
    return res