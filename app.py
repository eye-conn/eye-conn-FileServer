# importing the required libraries
import os
import sys
from flask import Flask, render_template, request, send_file, send_from_directory
from json import dumps, loads
import random

# initialising the flask app
app = Flask(__name__)

# Creating the upload folder
upload_folder = os.path.join(os.getcwd(), 'files','uploads',)
if not os.path.exists(upload_folder):
   os.mkdir(upload_folder)

# Creating the download folder
download_folder = os.path.join(os.getcwd(), 'files','downloads')
if not os.path.exists(download_folder):
   os.mkdir(download_folder)


def encrypt(file):
    try:
        fo = open(os.path.join(upload_folder,file), "rb")
        image=fo.read()
        fo.close()
        image=bytearray(image)
        key=random.randint(0,256)
        # key = bytearray(key)
        for index , value in enumerate(image):
            image[index] = value^key
        fo=open(os.path.join(download_folder,file[:-4]+'.eye'),"wb")
        imageRes="enc.jpg"
        fo.write(image)
        fo.close()
        if os.path.exists(os.path.join(upload_folder,file)):
            os.remove(os.path.join(upload_folder,file))
        return None,key
        # fin = open('hi.jpg', 'wb')
     
        # writing encrypted data in image
        # fin.write(image)
        # fin.close()
    except Exception as e:
        print(e)
        return "Error",None

def decrypt(file,key):
    try:
        fo = open(os.path.join(upload_folder,file), "rb")
        image=fo.read()
        fo.close()
        image=bytearray(image)
        for index , value in enumerate(image):
            image[index] = value^key
        fo=open(os.path.join(download_folder,file),"wb")
        imageRes="dec.jpg"
        fo.write(image)
        fo.close()
        if os.path.exists(os.path.join(upload_folder,file)):
            os.remove(os.path.join(upload_folder,file))
        return 
    except Exception as e:
        print(e)
        return 

# configuring the allowed extensions
allowed_extensions = ['jpg', 'png', 'jpeg']
def check_file_extension(filename):
    return filename.split('.')[-1] in allowed_extensions


@app.route('/encrypt', methods = ['GET', 'POST'])
def encryptFile():
    if request.method != 'GET': # check if the method is post
      try:
            file = request.form.get('file')+'.jpg'
            # key = request.form.get('key') 
        #   print(files.content_length,flush=True)
            # print(loads(request.data),flush=True)
            error,key=encrypt(file)
            print(key)
            return dumps({"success": True, "key": key})
      except Exception as e:
            print(e)
            return  dumps({"error": "Folder not found"})

    else:
        return dumps({"error": "Could not upload"})

@app.route('/decrypt', methods = ['GET', 'POST'])
def decryptFile():
    if request.method != 'GET': # check if the method is post
      try:
            file = request.form.get('file')+'.jpg'
            key = request.form.get('key') 
        #   print(files.content_length,flush=True)
            print(file,key)
            # print(loads(request.data),flush=True)
            decrypt(file, int(key))
            return dumps({"success": True})
      except Exception as e:
            print(e)
            return  dumps({"error": "Folder not found"})

    else:
        return dumps({"error": "Could not upload"})


# Sending the file to the user
@app.route('/download')
def download():
    try:
        # send file from encrypted directory
        return send_file(os.path.join(download_folder,request.args.get('file')), as_attachment=True)
    except Exception as e:
        print(e)
        return dumps({"error": "File not found"})

@app.route('/upload', methods = ['GET', 'POST'])
def uploadfile():
    if request.method != 'GET': # check if the method is post
      print(request.files)
      files = request.files.get('image') # get the file from the files object
    #   print(files.content_length,flush=True)
      try:
            files.save(os.path.join(upload_folder,files.filename))
            return dumps({"success": True})
      except FileNotFoundError:
            return  dumps({"error": "Folder not found"})

    else:
        return dumps({"error": "Could not upload"})

		
if __name__ == '__main__':
#    print current path
#    print(os.getcwd())
# print(os.path.join(os.getcwd(),"/files/encrypted/"), flush=True)
   app.run(threaded=True, debug=True) # running the flask app




