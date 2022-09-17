"""
Main function
"""
import json
from google.cloud import vision

def main(event, context):
    # print("event: ", event)
    # print("context: ", context)
    print("An image was uploaded")
    print("URL: gs://soa-projects-images/" + event["name"])
    pic = event["name"]
    uri_base = 'gs://soa-projects-images/'
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    # Names of likelihood from google.cloud.vision.enums
    likelihood = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY')    
    #image.source.image_uri = '%s/%s' % (uri_base, pic)
    image.source.image_uri = '%s/%s' % (uri_base,pic)
    response = client.face_detection(image=image)
    faces = response.face_annotations
    print('File:', pic)
    for face in faces:
        emotions2 = likelihood[face.anger_likelihood]
        emotions3 = likelihood[face.joy_likelihood]
        emotions4 = likelihood[face.sorrow_likelihood]
        emotions5 = likelihood[face.surprise_likelihood]
        emotions6 = likelihood[face.headwear_likelihood]
    emotions = {
        "Angry":emotions2,
        "Joy":emotions3,
        "Sorrow":emotions4,
        "Surprise":emotions5,
        "headwear":emotions6,
    }
    
    print(json.dumps(emotions))
    return json.dumps(emotions)