import wave
def encode_aud_data(audio_path,encrypted_text,name_of_file):
    song = wave.open(audio_path, mode='rb')
    nframes=song.getnframes()
    frames=song.readframes(nframes)
    frame_list=list(frames)
    frame_bytes=bytearray(frame_list)
    res = ''.join(format(i, '08b') for i in bytearray(encrypted_text, encoding ='utf-8'))     
    print("\nThe string after binary conversion :- " + (res))   
    length = len(res)
    print("\nLength of binary after conversion :- ",length)
    encrypted_text = encrypted_text + '*^*^*'
    result = []
    for c in encrypted_text:
        bits = bin(ord(c))[2:].zfill(8)
        result.extend([int(b) for b in bits])
    j = 0
    for i in range(0,len(result),1): 
        res = bin(frame_bytes[j])[2:].zfill(8)
        if res[len(res)-4]== result[i]:
            frame_bytes[j] = (frame_bytes[j] & 253)      #253: 11111101
        else:
            frame_bytes[j] = (frame_bytes[j] & 253) | 2
            frame_bytes[j] = (frame_bytes[j] & 254) | result[i]
        j = j + 1    
    frame_modified = bytes(frame_bytes)
    stego_file_name = 'stego_'+name_of_file
    with wave.open(stego_file_name, 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)   
    song.close()
    return stego_file_name