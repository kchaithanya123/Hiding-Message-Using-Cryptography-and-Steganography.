import os
import cv2
import wave
from cryptographyModule import encryption,decryption
from textSteganography import encodeTextIntoFile,extract_text_file
from imageSteganography import encode_img_data
from audioSteganograpy import encode_aud_data
from videoSteganography import encode_video_data,extractfromVideo
from flask import Flask, render_template,request
from conversions import msgtobinary

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.secret_key = 'Secret Key'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/text-steganography')
def text_steganography():
    return render_template('text-steganography.html')

@app.route('/image-steganography')
def image_steganography():
    return render_template('image-steganography.html')

@app.route('/audio-steganography')
def audio_steganography():
    return render_template('audio-steganography.html')

@app.route('/video-steganography')
def video_steganography():
    return render_template('video-steganography.html')



# Text steganography routes
@app.route('/text-steganography/encode', methods=['GET', 'POST'])
def text_encode():
    return render_template('text-encode.html')

#To embed text into given text file 
@app.route('/text-steganography/embed', methods=['GET', 'POST'])
def text_embed():    
    if request.method == 'POST':
        file = request.files['file']
        if not request.form.get('text'):
              return render_template('/text-encode.html',error = "Text area cant be empty")
        file_contents = file.read().decode('utf-8')
        words = file_contents.split()
        file_length = len(file_contents)
        print(file_length)
        key = request.form['key']
        text = request.form['text']
        encrypted_text = encryption (text,key)
        textarea_length = len(encrypted_text)
        if textarea_length <= (file_length//6):
            if key == '':
                return render_template('/text-encode.html',error = "Key must be provided")
            else:    
                encodeTextIntoFile(encrypted_text,words,file)
                return render_template('embed-text.html')
        else:
            return render_template('/text-encode.html',error = "Secret message is too lengthy to embed. Please shorten it.")
    return render_template('embed-text.html')


@app.route('/text-steganography/decode',methods=['GET', 'POST'])
def text_decode():
    return render_template('text-decode.html')

#To extract the message hidden in the text file
@app.route('/text-steganography/extract',methods=['GET', 'POST'])
def text_extract():
    if request.method == 'POST':
        file = request.files['stego-file']
        key = request.form['key']
        if key == '':
            return render_template('/text-encode.html',error = "Key must be provided")
        else: 
            decoded_message = extract_text_file(file,key) 
            return render_template("text-result.html",decoded_msg=decoded_message)
    return render_template('text-decode.html')
    


# Image steganography routes 
@app.route('/image-steganography/encode', methods=['GET', 'POST'])
def image_encode():
    return render_template('image-encode.html')

#To embed the message in the given image file
@app.route('/image-steganography/embed',methods=['GET', 'POST'])
def image_embed():
    if request.method == 'POST':
        image_file = request.files['file']
        name_of_file = image_file.filename
        image_path = 'uploads/' + image_file.filename
        image_file.save(image_path)
        if not request.form.get('text'):
              return render_template('/image-encode.html',error = "Text area cant be empty")
        key = request.form['key']
        text = request.form['text']
        encrypted_text = encryption (text,key)
        if key == '':
                return render_template('/image-encode.html',error = "Key must be provided")
        else:    
            encode_img_data(image_path,encrypted_text,name_of_file)
            return render_template('embed-text.html')
    return render_template('image-encode.html')
    


@app.route('/image-steganography/decode')
def image_decode():
    return render_template('image-decode.html')

#To extract the message hidden in the Image file
@app.route('/image-steganography/extract',methods=['GET', 'POST'])
def image_extract():
    if request.method == 'POST':
        file = request.files['stego-file']
        key = request.form['key']
        stego_file_name = file.filename       
        if key == '':
            return render_template('/image-encode.html',error = "Key must be provided")
        else: 
            data_binary = ""
            image=cv2.imread(stego_file_name)
            for i in image:
                for pixel in i:
                    r, g, b = msgtobinary(pixel) 
                    data_binary += r[-1]  
                    data_binary += g[-1]  
                    data_binary += b[-1]  
                    total_bytes = [ data_binary[i: i+8] for i in range(0, len(data_binary), 8) ]
                    decoded_data = ""
                    for byte in total_bytes:
                        decoded_data += chr(int(byte, 2))
                        
                        if decoded_data[-5:] == '*^*^*': 
                            print("\n\nThe Encoded  ",decoded_data[:-5])
                            message = decryption(decoded_data[:-5],key)
                            print(message)
                            return render_template("text-result.html",decoded_msg=message)
            return render_template("text-result.html")
    return render_template('image-decode.html')



# Audio steganography routes
@app.route('/audio-steganography/encode')
def audio_encode():
    return render_template('audio-encode.html')

#To embed the message in an Audio file
@app.route('/audio-steganography/embed',methods=['GET', 'POST'])
def audio_embed():
    if request.method == 'POST':
        audio_file = request.files['file']
        name_of_file = audio_file.filename
        audio_path = 'uploads/' +audio_file.filename
        audio_file.save(audio_path)
        if not request.form.get('text'):
            return render_template('/audio-encode.html',error = "Text area cant be empty")
        key = request.form['key']
        text = request.form['text']
        encrypted_text = encryption (text,key)
        if key == '':
                return render_template('/audio-encode.html',error = "Key must be provided")
        else:    
            encode_aud_data(audio_path,encrypted_text,name_of_file)
            return render_template('embed-text.html')

    return render_template('audio-encode.html')




@app.route('/audio-steganography/decode')
def audio_decode():
    return render_template('audio-decode.html')

#To extract the message from an Audio file
@app.route('/audio-steganography/extract',methods=['GET', 'POST'])
def audio_extract():
    if request.method == 'POST':
        file = request.files['stego-file']
        key = request.form['key']
        stego_file_name = file.filename
        if key == '':
            return render_template('/audio-encode.html',error = "Key must be provided")
        else: 
            song = wave.open(stego_file_name, mode='rb')
            nframes=song.getnframes()
            frames=song.readframes(nframes)
            frame_list=list(frames)
            frame_bytes=bytearray(frame_list)
            extracted = ""
            p=0
            for i in range(len(frame_bytes)):
                if(p==1):
                    break
                res = bin(frame_bytes[i])[2:].zfill(8)
                if res[len(res)-2]==0:
                    extracted+=res[len(res)-4]
                else:
                    extracted+=res[len(res)-1]            
                all_bytes = [ extracted[i: i+8] for i in range(0, len(extracted), 8) ]
                decoded_data = ""
                for byte in all_bytes:
                    decoded_data += chr(int(byte, 2))
                    if decoded_data[-5:] == "*^*^*":
                        data = decoded_data[:-5]
                        result = decryption(data,key)
                        print("The Encoded data was :--",result)
                        p=1
                        break  
            return render_template("text-result.html",decoded_msg=result)
    return render_template('audio-decode.html')



# Video steganography routes
@app.route('/video-steganography/encode')
def video_encode():
    return render_template('video-encode.html')

#To embed the message in a videofile
@app.route('/video-steganography/embed',methods=['GET', 'POST'])
def video_embed():
    if request.method == 'POST':
        video_file = request.files['file']
        name_of_file = video_file.filename
        video_path = 'uploads/' + video_file.filename
        video_file.save(video_path)
        if not request.form.get('text'):
              return render_template('/video-encode.html',error = "Text area cant be empty")
        key = request.form['key']
        text = request.form['text']
        frame = request.form['frame']
        frame_number = int(frame)
        encrypted_text = encryption (text,key)
        if key == '':
                return render_template('/video-encode.html',error = "Key must be provided")
        else:    
            encode_video_data(video_path,encrypted_text,name_of_file,frame_number)
            return render_template('embed-text.html')
    return render_template('video-encode.html')


@app.route('/video-steganography/decode')
def video_decode():
    return render_template('video-decode.html')

#To extract the message from video file
@app.route('/video-steganography/extract',methods=['GET', 'POST'])
def video_extract():
    if request.method == 'POST':
        file = request.files['stego-file']
        key = request.form['key']
        frame_number_selected = request.form['frame']
        stego_file_name = file.filename
        temp_name = 'frame_'+(file.filename[:-4])+'.png'
        if key == '':
            return render_template('/video-encode.html',error = "Key must be provided")
        else:
            video_file =  cv2.VideoCapture(stego_file_name)
            max_frame=0;
            while( video_file.isOpened()):
                ret, frame = video_file.read()
                if ret == False:
                        break
                max_frame+=1
            print("Total number of Frame in selected Video :",max_frame)
            n= int(frame_number_selected)
            vidcap = cv2.VideoCapture(stego_file_name)
            frame_number = 0
            while(vidcap.isOpened()):
                frame_number += 1
                ret, frame = vidcap.read()
                if ret == False:
                    break
                if frame_number == n:                    
                    image=cv2.imread(temp_name)
                    message = extractfromVideo(image,key)
                    return render_template("text-result.html",decoded_msg=message)
    return render_template('video-decode.html')


if __name__ == '__main__':
    app.run()
