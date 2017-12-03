import sys
from os import path
# import parent directory into path so that origami can be imported
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import origami
import numpy as np
import cv2      # for reading image files

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
    # test number: 
    # 0 for text array, 
    # 1 for image array using filepath, 
    # 2 for image array using np array, 
    # 3 for all
    tnum = origami.request.form['test_number']

    if tnum == '0' or tnum == '3':
        print('hello')
        # test getTextArray
        all_text = origami.getTextArray()
        print('Received %d text strings'%(len(all_text)))
        print(all_text)
        # check that number of entries received is correct
        if len(all_text) != len(text_list):
            return 'Wrong number of strings received', 500
        # check that strings received match expected strings
        if all_text != text_list:
            return 'Text data not received correctly', 500        
    
    if tnum == '1' or tnum == '3':
        # test getImageArray with file_path mode
        all_image_paths = origami.getImageArray(mode='file_path')
        print('Received %d image paths'%(len(all_image_paths)))
        print(all_image_paths)
        # check that number of entries received is correct
        if len(all_image_paths) != len(image_list):
            return 'Wrong number of images received', 500
        # check that images are correctly decoded into numpy arrays
        for i in range(len(all_image_paths)):
            im1 = cv2.imread(all_image_paths[i])
            im2 = cv2.imread(image_list[i])
            # check that images match in shape and pixel values
            if not np.array_equal(im1, im2):
                return 'Images not saved correctly', 500
    
    if tnum == '2' or tnum == '3':
        # test getImageArray with numpy_array mode
        all_images = origami.getImageArray(mode='numpy_array')
        # check that number of entries received is correct
        if len(all_images) != len(image_list):
            return 'Wrong number of images received', 500
        # check that images are saved correctly into given filepaths
        for i in range(len(all_images)):
            im = cv2.imread(image_list[i])
            # check that images match in shape and pixel values
            if not np.array_equal(all_images[i], im):
                return 'Images not converted correctly', 500

    return 'OK'

app.run()
