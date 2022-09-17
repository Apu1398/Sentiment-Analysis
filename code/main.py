import json
from google.cloud import vision
from google.cloud import storage

'''
Main Function
'''

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
        #print(f'Angry likelyhood: {likelihood[face.anger_likelihood]}')         
        #print(f'Joy Likelyhood: {likelihood[face.joy_likelihood]}')             
        #print(f'Sorrow likelyhood {likelihood[face.sorrow_likelihood]}')        
        #print(f'Surprised likelyhood {likelihood[face.surprise_likelihood]}')   
        #print(f'Headwear likelyhood {likelihood[face.headwear_likelihood]}')   


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

    # read the database
    
    try:
        blob = bucket.get_blob(database_filename)
        database_json = json.loads(blob.download_as_string())
    except:
        database_json = []
        
    # write in database
    
    database_json.append(emotions)    
    blob = bucket.blob(database_filename)    
    # take the upload outside of the for-loop otherwise you keep overwriting the whole file
    # blob.upload_from_string(data=json.dumps(emotions), content_type='application/json') 
    blob.upload_from_string(data=json.dumps(database_json), content_type='application/json') 
    return json.dumps(emotions)
