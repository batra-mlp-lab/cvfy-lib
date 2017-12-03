import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import origami
import cv2

app = origami.register('gh:127.0.0.1:1:1:8888:0.0.0.0')

image_list = [
    'example1.png',
    'example2.png'
]

@origami.crossdomain
@app.listen()
def test():
    all_image_paths = origami.getImageArray(mode='file_path')
    all_images = origami.getImageArray(mode='numpy_array')
    all_text = origami.getTextArray()
    print('Received %d image paths'%(len(all_image_paths)))
    print('Received %d text strings'%(len(all_text)))
    print(all_image_paths)
    print(all_text)
    assert(len(all_image_paths) == len(image_list))
    assert(len(all_images) == len(image_list))
    assert(len(all_text) == 3)
    assert(all_text == ['hello', 'world', 'Is this a sample question?'])
    for i in range(len(all_images)):
        assert((all_images[i] == cv2.imread(image_list[i])).all())
    for i in range(len(all_image_paths)):
        assert((cv2.imread(all_image_paths[i]) == cv2.imread(image_list[i])).all())
    print('Test passed')
    return 'OK'

app.run()

