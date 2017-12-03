import requests 

# server running locally at port 8888
url = 'http://127.0.0.1:8888/event'

# text data to be sent
data = {
    'input-text-0': 'hello',
    'input-text-1': 'world',
    'input-text-2': 'Is this a sample question?',
    'input-text-4': 'This will not be read'
}
# list of images to be sent
image_list = [
    'example1.png',
    'example2.png'
]

def test_sendText():
    data_copy = data.copy()
    data_copy['test_number'] = 0
    r = requests.post(url=url, data=data_copy)
    print(r)

def test_sendImage_filepath():
    # compile image data as byte strings
    files = {}
    for i in range(len(image_list)):
        with open(image_list[i], 'rb') as f:
            files['input-image-%d'%(i)] = f.read()
    r = requests.post(url=url, files=files, data={'test_number': 1})    
    print(r)

def test_sendImage_nparray():
    # compile image data as byte strings
    files = {}
    for i in range(len(image_list)):
        with open(image_list[i], 'rb') as f:
            files['input-image-%d'%(i)] = f.read()
    r = requests.post(url=url, files=files, data={'test_number': 2})
    print(r)

def test_all():
    data_copy = data.copy()
    data_copy['test_number'] = 3
    files = {}
    for i in range(len(image_list)):
        with open(image_list[i], 'rb') as f:
            files['input-image-%d'%(i)] = f.read()
    r = requests.post(url=url, files=files, data=data_copy)
    print(r)
