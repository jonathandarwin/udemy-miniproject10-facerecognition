import cv2
import numpy as np
from os import listdir
from os.path import isfile, join

# Get the training data we previously made
data_path = 'faces/user/'
onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]

# Create arrays for training data and labels
Training_Data, Labels = [], []

# Open training images in our datapath
# Create a numpy array for training data
for i, files in enumerate(onlyfiles):
    image_path = data_path + onlyfiles[i]
    images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    Training_Data.append(np.asarray(images, dtype=np.uint8))
    Labels.append(i)

Labels = np.asarray(Labels, dtype=np.int32)

model = cv2.face.LBPHFaceRecognizer_create()
model.train(np.asarray(Training_Data), np.asarray(Labels))
print('Model trained sucessefully')


face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def face_detector(img, size=0.5):
    
    # Convert image to grayscale
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # detect face menggunakan haar cascade
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    if faces is ():
        return img, []
    
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
        roi = img[y:y+h, x:x+w]
        roi = cv2.resize(roi, (200, 200))
    return img, roi


# Open Webcam
cap = cv2.VideoCapture(0)
text = ''
color = ()
while True:

    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    image, face = face_detector(frame)
    
    try:
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        # Pass face to prediction model
        # 'results' comprises of a tuple containing the label and the confidence value
        results = model.predict(face)
        
        if results[1] < 500:
            confidence = int( 100 * (1 - (results[1])/400) )
            display_string = str(confidence) + '% Confident it is User'
            
        cv2.putText(image, display_string, (100, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (255,120,150), 2)
        
        # confidence : seberapa yakin algoritma terhadap hasil yang dikeluarkan
        # biasanya di set kalo diatas 75 itu jawaban ny valid
        if confidence > 75:
            text = 'Unlocked'   
            color = (0,255,0)         
        else:
            text = 'Locked'
            color = (0,0,255)         

    except:
        text = 'Locked'
        color = (0,0,255)     
        cv2.putText(image, 'No Face Found', (220, 120) , cv2.FONT_HERSHEY_COMPLEX, 1, color, 2)        
        pass

    cv2.putText(image, text, (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, color, 2)
    cv2.imshow('Face Recognition', image)
        
    if cv2.waitKey(1) == 13: #13 is the Enter Key
        break
        
cap.release()
cv2.destroyAllWindows() 