import cv2
from conversions import msgtobinary
def encode_img_data(image_path,encrypted_text,name_of_file):
    cover_image = cv2.imread(image_path)
    height, width, channels = cover_image.shape

    # Calculate the total number of pixels needed to encode the secret message
    num_pixels = height * width * channels
    max_embedding = num_pixels // 8
    print("Max embed: ",max_embedding)
    if(len(encrypted_text)>max_embedding):
        raise ValueError("Insufficient bytes Error, Need Bigger Image or give Less Data !!")   
    encrypted_text +='*^*^*'       
    binary_data=msgtobinary(encrypted_text)
    length_data=len(binary_data)   
    print("\nThe Length of Binary data",length_data)   
    index_data = 0
    
    for i in cover_image:
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
    stego_file_name = 'stego_'+name_of_file
    cv2.imwrite(stego_file_name,cover_image)
    print("\nEncoded the data successfully in the Image and the image is successfully saved.")
    return stego_file_name
