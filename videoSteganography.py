import cv2
from cryptographyModule import decryption
from conversions import msgtobinary

def encode_video_data(video_path,encrypted_text,name_of_file,frame_number_selected):
    cap=cv2.VideoCapture(video_path)
    vidcap = cv2.VideoCapture(video_path)    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    frame_width = int(vidcap.get(3))
    frame_height = int(vidcap.get(4))
    size = (frame_width, frame_height)
    stego_video_name = 'stego_'+name_of_file
    out = cv2.VideoWriter( stego_video_name,fourcc, 25.0, size)
    max_frame=0;
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        max_frame+=1
    cap.release()
    print("Total number of Frame in selected Video :",max_frame)
    n=frame_number_selected
    frame_number = 0
    while(vidcap.isOpened()):
        frame_number += 1
        ret, frame = vidcap.read()
        if ret == False:
            break
        if frame_number == n:    
            change_frame_with = embed(frame,encrypted_text)
            frame_ = change_frame_with
            frame = change_frame_with
        out.write(frame)    
    print("\nEncoded the data successfully in the video file.") 
    name_of_file_after = name_of_file[:-4]
    stego_frame_name = 'frame_stego_'+name_of_file_after+'.png'
    cv2.imwrite( stego_frame_name, frame_)  
   


def embed(frame,encrypted_text):
        data= encrypted_text
        print("The encrypted data is : ",data)
        if (len(data) == 0): 
            raise ValueError('Data entered to be encoded is empty')
        data +='*^*^*'        
        binary_data=msgtobinary(data)
        length_data = len(binary_data)       
        index_data = 0        
        for i in frame:
            for pixel in i:
                r, g, b = msgtobinary(pixel)
                if index_data < length_data:
                    pixel[0] = int(r[:-1] + binary_data[index_data], 2) 
                    index_data += 1
                if index_data < length_data:
                    pixel[1] = int(g[:-1] + binary_data[index_data], 2) 
                    index_data += 1
                if index_data < length_data:
                    pixel[2] = int(b[:-1] + binary_data[index_data], 2) 
                    index_data += 1
                if index_data >= length_data:
                    break
            return frame

def extractfromVideo(image,key):
    data_binary = ""
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
                    return message    