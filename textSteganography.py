from cryptographyModule import decryption
from conversions import BinaryToDecimal
def encodeTextIntoFile(text,word,file):
    print(text)
    res1 = ''.join([ format(ord(i), "012b") for i in text])
    res1=res1+"111111111111"
    print("The string after binary conversion appyling all the transformation :- " + (res1))   
    length = len(res1)
    print("Length of binary after conversion:- ",length)
    HM_SK=""
    ZWC={"00":u'\u200C',"01":u'\u202C',"11":u'\u202D',"10":u'\u200E'}      
    new_file_path = "encrypted_" + file.filename
    with open(new_file_path, "w+", encoding="utf-8") as file3:
            i=0
            while(i<len(res1)):  
                s=word[int(i/12)]
                j=0
                x=""
                HM_SK=""
                while(j<12):
                    x=res1[j+i]+res1[i+j+1]  #res1 has binary encoded secret message
                    HM_SK+=ZWC[x]
                    j+=2
                s1=s+HM_SK
                file3.write(s1)
                file3.write(" ")
                i+=12
            t=int(len(res1)/12) 
            while t<len(word): 
                file3.write(word[t])
                file3.write(" ")
                t+=1
            file3.close()  
            print("\nStego file has successfully generated")
    return new_file_path



def extract_text_file(file,key):
    ZWC_reverse={u'\u200C':"00",u'\u202C':"01",u'\u202D':"11",u'\u200E':"10"}
    temp = ''       
    for line in file:
        line=line.decode()
        for words in line.split():
            T1 = words
            binary_extract=""
            for letter in T1:
                if(letter in ZWC_reverse):
                    binary_extract+=ZWC_reverse[letter]
            if binary_extract=="111111111111":
                break
            else:
                temp+=binary_extract
    print("\nEncrypted message presented in code bits:",temp) 
    lengthd = len(temp)
    print("\nLength of encoded bits:- ",lengthd)
    a=0
    b=12
    i=0
    final = ""
    print("temp: "+temp)
    while i<len(temp):
        t3=temp[a:b]
        a+=12
        b+=12
        i+=12
        decimal_data = BinaryToDecimal(t3)
        final+=chr(decimal_data)
    print("\nMessage after decoding from the stego file:- ",decryption(final,key))
    return decryption(final,key)

