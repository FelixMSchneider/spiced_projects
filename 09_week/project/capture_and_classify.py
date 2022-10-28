import sys
import logging
import os
import cv2
from utils import write_image, key_action, init_cam
import pylab as plt
import numpy as np
import PIL.Image
import tensorflow as tf
# clean classify_folder

classify_folder="./classify"
os.system("mkdir -p " + classify_folder)

def clean_classify_folder():
    os.system("rm -f classify/*.png") 


def get_and_preprocess_image(imagefile):
    with PIL.Image.open(imagefile) as myimage:
        im_array = np.array(myimage)

    pp_im=tf.keras.applications.mobilenet_v2.preprocess_input(im_array)
    xtest=np.array([np.array(pp_im),])
    return xtest

CLASSES = ['Shoes', 'Spoons', 'Books', 'Forks'] #os.listdir('./data/Trainimages')

model = tf.keras.models.load_model('my_model.h5')

# define an image data generator
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
data_gen = tf.keras.preprocessing.image.ImageDataGenerator(preprocessing_function=preprocess_input)




if __name__ == "__main__":

    # folder to write images to
    #out_folder = sys.argv[1]

    # maybe you need this
    os.environ['KMP_DUPLICATE_LIB_OK']='True'

    logging.getLogger().setLevel(logging.INFO)
   
    # also try out this resolution: 640 x 360
    webcam = init_cam(640, 480)
    key = None

    try:
        # q key not pressed 
        while key != 'q':
            # Capture frame-by-frame
            ret, frame = webcam.read()
            # fliping the image 
            frame = cv2.flip(frame, 1)
   
            # draw a [224x224] rectangle into the frame, leave some space for the black border 
            offset = 2
            width = 224
            x = 160
            y = 120
            cv2.rectangle(img=frame, 
                          pt1=(x-offset,y-offset), 
                          pt2=(x+width+offset, y+width+offset), 
                          color=(0, 0, 0), 
                          thickness=2
            )     
            
            # get key event
            key = key_action()
            
            if key == 'space':
                # write the image without overlay
                # extract the [224x224] rectangle out of it
                image = frame[y:y+width, x:x+width, :]
                write_image(classify_folder, image) 

            if key == 'p':

                clean_classify_folder()
                image = frame[y:y+width, x:x+width, :]
                write_image(classify_folder, image)

                import glob
                imlist=glob.glob(classify_folder+"/*.png")

                xtest=get_and_preprocess_image(imlist[0])

                pred=model.predict(xtest, verbose = 0)
                ind=np.argmax(pred[0])
                print(" what you are showing  is most probable a "+ CLASSES[ind])



            # disable ugly toolbar
            cv2.namedWindow('frame', flags=cv2.WINDOW_GUI_NORMAL)              
            
            # display the resulting frame
            cv2.imshow('frame', frame)            
            
    finally:
        # when everything done, release the capture
        logging.info('quit webcam')
        webcam.release()
        cv2.destroyAllWindows()
