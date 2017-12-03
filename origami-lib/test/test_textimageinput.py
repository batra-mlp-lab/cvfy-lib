import requests 

def test_sendTextAndImage():
    # server running locally at port 8888
    url = 'http://127.0.0.1:8888/event'
    # list of images to be sent
    image_list = [
        'example1.png',
        'example2.png'
    ]
    # text data to be sent
    data = {
        'input-text-0': 'hello',
        'input-text-1': 'world',
        'input-text-2': 'Is this a sample question?',
        'input-text-4': 'This will not be read'
    }
    # compile image data as byte strings
    files = {}
    for i in range(len(image_list)):
        with open(image_list[i], 'rb') as f:
            files['input-image-%d'%(i)] = f.read()
    # send post request
    # files will be sent under request.files
    # text data will be sent under request.form
    r = requests.post(url=url, files=files, data=data)
    # print server response
    print(r)


