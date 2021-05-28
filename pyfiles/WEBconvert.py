import urllib.request
import numpy as np
import cv2
import os

def compress_img_CV(img, compress_rate=0.5):
    #name = path[len('../static/videoFaces/'):][:-4]
    #img = cv2.imread(path)
    heigh, width = img.shape[:2]
    img_resize = cv2.resize(img, (int(heigh*compress_rate), int(width*compress_rate)),interpolation=cv2.INTER_AREA)
    #cv2.imwrite('../static/compressedCover/' + name+'.jpg', img_resize)
    #print("%s Compressed，" % (name), "压缩率：", compress_rate)
    return img_resize

def url_to_image(url):
  # download the image, convert it to a NumPy array, and then read
  # it into OpenCV format
  resp = urllib.request.urlopen(url, timeout=5)
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
    imgR = compress_img_CV(img_new)
    cv2.imwrite(path, imgR)
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