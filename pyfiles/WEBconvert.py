import urllib.request
import numpy as np
import cv2
import os
def url_to_image(url):
  # download the image, convert it to a NumPy array, and then read
  # it into OpenCV format
  resp = urllib.request.urlopen(url)
  image = np.asarray(bytearray(resp.read()), dtype="uint8")
  image = cv2.imdecode(image, cv2.IMREAD_COLOR)
 
  # return the image
  return image

def img_deal(url,path):
    if os.path.exists(path):
        return
    if url == "None" or url == "":
        print(url)
        print(path)
        return
    if url[-4:]!=".png" and url[-4:]!=".jpg":
        print(url)
        print(path)
        return
    img = url_to_image(url)
    rows, cols, channel = img.shape

    img_new = np.zeros((rows,cols,4),np.uint8)
    img_new[:,:,0:3] = img[:,:,0:3]

    img_circle = np.zeros((rows,cols,1),np.uint8)
    img_circle[:,:,:] = 0  
    #print(type(img_circle))
    #print(type(cols/2))
    
    img_circle = cv2.circle(img_circle,(cols//2,rows//2),min(rows, cols)//2,(255),-1) 

    img_new[:,:,3] = img_circle[:,:,0]
    cv2.imwrite(path, img_new)
    #print(path)

def cover_deal(url,path):
    if os.path.exists(path):
        return
    if url == "None" or url == "":
        print(path)
        return
    img = url_to_image(url)
    cv2.imwrite(path, img)
    
if __name__ == "__main__":
    path = "http://i0.hdslb.com/bfs/face/27f0467f90da15f399ee399bb7c5dff08f0fe048.jpg"
    #cv2.imwrite('1.png', img_deal(path))