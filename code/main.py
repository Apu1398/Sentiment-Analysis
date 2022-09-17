def main(event, context):
    # print("event: ", event)
    # print("context: ", context)
    print("An image was uploaded")
    
    
    print("URL: https://storage.cloud.google.com/soa-2022-360315-images/" + event["name"])
    