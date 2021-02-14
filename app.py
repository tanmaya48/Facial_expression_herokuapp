from flask import Flask, render_template, request
import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

image = cv2.imread('glasses.png',cv2.IMREAD_COLOR)
row, col , channels = image.shape


def set_image(img,eyes,x,y):

   print('gfgfgf'+str(eyes))

   flag = 0

   if (len(eyes) == 2):   ## if two eyes are found... sometimes objects are misidentified as eyes, and sometimes eyes are not identified 

        flag = 1

        fx = eyes[0,0]+eyes[1,0] 
        fx= int(fx/2 + x)
        fy = eyes[0,1]+eyes[1,1] 
        fy= int(fy/2 + y)

        dis = abs(eyes[0,0]-eyes[1,0])
        print(fx,' ',fy,' ',dis)

        
        dis_default = 65 # default distance for the scale of glasses
        dx = 50 # rows offset
        dy = 20 # columns offset
        


        ratio = dis/dis_default

        dx = int(dx*ratio)  # shifting offsets to distance
        dy = int(dy*ratio)

        size = (int(col*ratio) , int(row*ratio) )

        print(ratio,' ',size)

        img3 = cv2.resize(image,size) 

        rows, cols , channels = img3.shape

        img3gray = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img3gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)     

   if flag == 1: # flag is used to wait for initial position of glasses to be set
        roi = img[fy+0-dy:fy+rows-dy,fx+0-dx:fx+cols-dx]  
        img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
        img3_fg = cv2.bitwise_and(img3,img3,mask = mask)
        dst = cv2.add(img1_bg,img3_fg)
        img[fy+0-dy:fy+rows-dy, fx+0-dx:fx+cols-dx] = dst 

   return img    





app = Flask(__name__)

@app.route('/')
def upload():
   return render_template('upload.html')




	
@app.route('/uploaded', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      name = f.filename
      f.save('static/'+name)

   img = cv2.imread('static/'+name) 
   gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

   faces = face_cascade.detectMultiScale(gray, 1.3, 5)

   for (x,y,w,h) in faces:
      #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

      roi_gray = gray[y:y+h, x:x+w]
      roi_color = img[y:y+h, x:x+w]
        
      eyes = eye_cascade.detectMultiScale(roi_gray)

      img = set_image(img,eyes,x,y)


   
   cv2.imwrite('static/'+name,img) 

   print('expression has been determined')

   return render_template('output.html',filename = name)



		
if __name__ == '__main__':
   app.run(debug = False)