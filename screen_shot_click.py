from PIL import ImageGrab  # PIL is windows machine only.
from PIL import Image
from numpy import array, unravel_index, argmax
from scipy.signal import correlate
from scipy.signal import correlate2d
import matplotlib.pyplot as plt
import win32api, win32con
import time

# helping function for clicking
def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    win32api.keybd_event(0x0D, 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(0x0D, 0, win32con.KEYEVENTF_KEYUP, 0)

# capture full screen
screen = ImageGrab.grab()  # screen

# as a test, launch atom using the desktop icon
icon = Image.open(r"image_resources\keepass_icon.PNG")  # icon to find


# using rolling window method
haystack = array(screen.convert('RGB'))
needle = array(icon.convert('RGB'))
max_dim = haystack.shape
min_dim = needle.shape

#hay = list(haystack.flatten())
#need = list(needle.flatten())

#for loop_num in range(len(hay) - len(need)):
#    if hay[loop_num:loop_num+len(need)] == need:
#        print('yes')






# use correlate to find match
print('optimized correlate method')
haystack = array(screen.convert('L'))
m_val = haystack.mean(dtype='uint8')
haystack -= m_val
needle = array(icon.convert('L'))
needle = needle - needle.mean()
print(haystack.shape)

#c = correlate(haystack, needle, mode='same')  # to heavy
print('starting correlation calculation')
corr = correlate2d(haystack, needle, boundary='symm', mode='same')
print('done correlating')
#plt.imshow(corr)
#plt.figure()
#plt.imshow(haystack)
#plt.figure()
#plt.imshow(needle)
#plt.gray()
#i = Image(corr)
#plt.show()
v,h = unravel_index(argmax(corr), corr.shape)
print(corr)
print(h,v)

# move mouse to coordinates
win32api.SetCursorPos((h,v))
click(h,v)



