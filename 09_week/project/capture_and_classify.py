import logging
import os
import cv2
from utils import write_image, key_action, init_cam
import numpy as np
import PIL.Image
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

def get_and_preprocess_image(imagefile):
    with PIL.Image.open(imagefile) as myimage:
        im_array = np.array(myimage)

    pp_im=tf.keras.applications.mobilenet_v2.preprocess_input(im_array)
    xtest=np.array([np.array(pp_im),])
    return xtest

CLASSES = ['shoe', 'spoon', 'book', 'fork', ] #os.listdir('./data/Trainimages')

classify_folder="./classify"
os.system("mkdir -p " + classify_folder)

# load the trained model
model = tf.keras.models.load_model('my_model.h5')


if __name__ == "__main__":

    # maybe you need this
    os.environ['KMP_DUPLICATE_LIB_OK']='True'
    logging.getLogger().setLevel(logging.INFO)
   

    webcam = init_cam(640, 480)
    key = None
    ind=-1
    loopcnt=0

    try:

        while True:
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
            if ind>=0:
                # ind is > 0 if classification has been done --> put result as text on frame 
                # variables defined below! (previous loop after prediction)    
                frame=cv2.putText(frame, text, org, font, fontScale, color, thickness) 
                loopcnt+=1
                if loopcnt>100: # let text be displayed for 100 loops (may be adjusted)
                    loopcnt=0
                    ind=-1

   
            # disable ugly toolbar
            cv2.namedWindow('frame', flags=cv2.WINDOW_GUI_NORMAL)              
    
            # get key event
            key = key_action()
            
            if key == 'p':
                # classify the object which is currently shown to the camera

                image = frame[y:y+width, x:x+width, :]
                write_image(classify_folder, image, filename="current")
    
                xtest=get_and_preprocess_image(classify_folder+"/current.png")
    
                pred=model.predict(xtest, verbose = 0)
                ind=np.argmax(pred[0])
    
                print(" what you are showing is most probably a "+ CLASSES[ind].upper())

                ## PUT RESULT AS TEXT ON THE FRAME
                font = cv2.FONT_HERSHEY_SIMPLEX
                text = CLASSES[ind].upper()
                fontScale = 3
                thickness = 2
                color = (255, 0, 0)
    
                # get boundary of this text
                textsize = cv2.getTextSize(text, font, fontScale, thickness)[0]
    
                # center text
                textX = int(160+112 - textsize[0]/2)
                textY = int(120+112 + textsize[1]/2)
    
                org = (textX, textY)
                newframe=cv2.putText(frame, text, org, font, fontScale, color, thickness) 
                write_image(classify_folder, newframe)
                
            elif key == 'q':
                break

            else:    
                cv2.imshow('frame', frame)            
    
    finally:
        # when everything done, release the capture
        logging.info('quit webcam')
        webcam.release()
        cv2.destroyAllWindows()

