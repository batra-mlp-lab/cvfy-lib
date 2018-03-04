import requests 
import json
import numpy as np
import cv2


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


def test_saveTextArrayToCache():
    data_copy = data.copy()
    data_copy['test_number'] = 4
    r = requests.post(url=url, data=data_copy)

    
def test_checkIfCachedResultsExist():
    data_copy = data.copy()
    data_copy['test_number'] = 5
    r = requests.post(url=url, data=data_copy)
    exist= json.loads(r.content)['exist']
    assert(exist == True)


def test_loadTextArrayToCache():
    data_copy = data.copy()
    data_copy['test_number'] = 6
    r = requests.post(url=url, data=data_copy)
    text_array = json.loads(r.content)['text']
    assert(text_array == ['hello', 'world', 'Is this a sample question?'])


def test_saveImageArrayToCache_file_path():
    files = {}
    for i in range(len(image_list)):
        with open(image_list[i], 'rb') as f:
            files['input-image-%d'%(i)] = f.read()
    r = requests.post(url=url, files=files, data={'test_number': 7})
    text_array = json.loads(r.content)['text']
    assert(text_array == 'done')


def test_saveImageArrayToCache_np_array():
    files = {}
    al=[]
    for i in range(len(image_list)):
        with open(image_list[i], 'rb') as f:
            files['input-image-%d'%(i)] = f.read()
            al.append(f.read())
    r = requests.post(url=url, files=files, data={'test_number': 8})
    text_array = json.loads(r.content)['text']
    assert(text_array == 'done')


def test_loadImageArrayFromCache():
    files = {}
    for i in range(len(image_list)):
        with open(image_list[i], 'rb') as f:
            files['input-image-%d'%(i)] = f.read()
            
    r = requests.post(url=url, files=files,data={'test_number': 9})
    img_array = json.loads(r.content)['img']
    assert(len(img_array) == 4)  #2 for cache by file_path and 2 for cache by np_array




