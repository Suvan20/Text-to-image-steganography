import string
from PIL import Image
import numpy as np
import time
import base64


# Function that converts decimal values to binary
def decimal_to_binary(val):
    bin = 0
    counter = 0
    temp = val
    while (temp > 0):
        bin = ((temp % 2) * (10 ** counter)) + bin
        temp = int(temp / 2)
        counter += 1
    return bin

# Opening image using PIL library of Python
im = Image.open('cat_image_lower_pixels.jpg', 'r')


# Taking text to be hidden as input
input_text = str(input("Enter text to be hidden: "))

start_time = time.time()
# Creating a numpy array of pixel values for every pixel in image
pix = np.array(im, dtype = object)

# Converting the numpy array integer values to binary
x = np.vectorize(np.binary_repr)(pix, width=8)

# Reshaping the 3d numpy array to 2 dimensions of (h x w) and 3(r,g,b)
y = np.reshape(x,(x.shape[0] * x.shape[1],3))


input_text = input_text.encode("ascii")
input_text = base64.b64encode(input_text)
input_text = input_text.decode("ascii")

# Finding length of input text
length_of_text = len(input_text)

# Type casting to string
length_of_text = str(length_of_text)

# Representing text length in 10 characters
while (len(length_of_text) < 10):
    length_of_text = '0' + length_of_text


# Converting taken text into binary values
def convert_text(ip_text):
    final_array = []
    for char in ip_text:
        correction_factor = str(decimal_to_binary(ord(char)))
        while (len(correction_factor) < 8):
            correction_factor = '0' + correction_factor
        final_array.append(correction_factor)
    return final_array

# Forming array of length of text
length_array = convert_text(length_of_text)


# Calling function to get binary values of input text
array_of_binary_values = convert_text(input_text)


# Replacing the last two bits of pixel value with required binary values of text
def replace_two(np_array, array_of_bin):
    for i in range (2 * len(array_of_bin)):
        if (i%2 == 0):
            temp = extract_from_main_array(array_of_bin[i//2])
        for j in range (2):
            if (i % 2 == 0):
                if(j == 0):
                    np_array[i,j] = np_array[i,j][:6] + temp[0]
                else:
                    np_array[i,j] = np_array[i,j][:6] + temp[1]
            else:
                if (j == 0):
                    np_array[i,j] = np_array[i,j][:6] + temp[2]
                else:
                    np_array[i,j] = np_array[i,j][:6] + temp[3]
    
    for i in range (4*10):
        if (i%4 == 0):
            temp = extract_from_main_array(length_array[i//4])
        if (i%4 == 0):
            np_array[i,2] = np_array[i,2][:6] + temp[0]
        elif (i%4 == 1):
            np_array[i,2] = np_array[i,2][:6] + temp[1]
        elif (i%4 == 2):
            np_array[i,2] = np_array[i,2][:6] + temp[2]
        elif (i%4 == 3):
            np_array[i,2] = np_array[i,2][:6] + temp[3]

    return np_array

# Extracting 2 bits at a time from 8 bit value
def extract_from_main_array(main_array):
    temp = []
    temp.append(main_array[0:2])
    temp.append(main_array[2:4])
    temp.append(main_array[4:6])
    temp.append(main_array[6:])
    return temp

# Calling final function to add text to image
y = replace_two(y, array_of_binary_values)


# Obtain the original dimensions of the image
h, w = im.size
z = np.zeros((w,h,3),dtype=object)
z.flags.writeable = True
z = np.reshape(y, (w, h, 3))


# Converting every value in array to decimal value from binary
for i in range (im.height):
    for j in range (im.width):
        for k in range (3):
            z[i,j,k] = int(z[i,j,k],2)



# Converting data type from string to np.uint8
z = z.astype(np.uint8)


# Building an image using array of modified pixel values
reconstructed_image = Image.fromarray(z)

# Saving final image in which text is embedded
reconstructed_image.save('cat_image_lower_pixels_reconstructed.png')
end_time = time.time()

elapsed_time = end_time - start_time

print(elapsed_time)
