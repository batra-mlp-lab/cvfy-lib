import requests

def test_sendTextAndImage():
    url = 'http://127.0.0.1:8888/event'
    image_list = [
        'example1.png',
        'example2.png'
    ]
    data = {
        'input-text-0': 'hello',
        'input-text-1': 'world',
        'input-text-2': 'Is this a sample question?',
        'input-text-4': 'This will not be read'
    }
    files = {}
    for i in range(len(image_list)):
        with open(image_list[i], 'rb') as f:
            files['input-image-%d'%(i)] = f.read()
    r = requests.post(url=url, files=files, data=data)
    print(r)

