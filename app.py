from flask import Flask, render_template, request
import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')




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
      cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
   
   cv2.imwrite('static/'+name,img) 

   print('expression has been determined')

   return render_template('output.html',filename = name)



		
if __name__ == '__main__':
   app.run(debug = False)