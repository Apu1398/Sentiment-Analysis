'''
Important modules
'''
import json
from google.cloud import vision
from google.cloud import storage

'''
Main Function
'''
def main(event, context):
    pic = event["name"]
    uri_base = 'gs://soa-projects-images/'
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    likelihood = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY')
    image.source.image_uri = f'{uri_base}/{pic}'
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
    bucket_name = 'soa-projects-database'
    database_filename = 'data.json'
    bucket = storage.Client().get_bucket(bucket_name)
    database_json = []

    try:
        blob = bucket.get_blob(database_filename)
        database_json = json.loads(blob.download_as_string())
    except:
        database_json = []

    database_json.append(emotions)    
    blob = bucket.blob(database_filename)
    blob.upload_from_string(data=json.dumps(database_json), content_type='application/json')
    return json.dumps(emotions)
