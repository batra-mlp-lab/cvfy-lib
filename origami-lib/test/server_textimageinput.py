import sys
from os import path
# import parent directory into path so that origami can be imported
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import origami
# cv2 for reading image files
import cv2

# running at 127.0.0.1
# port 8888
app = origami.register('gh:127.0.0.1:1:1:8888:0.0.0.0')

# list of images to be received
image_list = [
    'example1.png',
    'example2.png'
]

# list of text to be received
text_list = [
    'hello',
    'world',
    'Is this a sample question?'
]

@origami.crossdomain
@app.listen()
def test():
    # test getImageArray with file_path mode
    all_image_paths = origami.getImageArray(mode='file_path')
    # test getImageArray with numpy_array mode
    all_images = origami.getImageArray(mode='numpy_array')
    # test getTextArray
    all_text = origami.getTextArray()
    # log details
    print('Received %d image paths'%(len(all_image_paths)))
    print('Received %d text strings'%(len(all_text)))
    print(all_image_paths)
    print(all_text)

    # check that the number of text strings and images received is correct
    assert(len(all_image_paths) == len(image_list))
    assert(len(all_images) == len(image_list))
    assert(len(all_text) == len(text_list))

    # check that the data are all processed properly
    assert(all_text == text_list)
    for i in range(len(all_images)):
        assert((all_images[i] == cv2.imread(image_list[i])).all())
    for i in range(len(all_image_paths)):
        assert((cv2.imread(all_image_paths[i]) == cv2.imread(image_list[i])).all())
    return 'OK'

app.run()

