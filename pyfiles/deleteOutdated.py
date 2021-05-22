import os,time

 
modifiedTime = time.localtime(os.stat("D:/mm.cfg").st_mtime)
createdTime = time.localtime(os.stat("D:/mm.cfg").st_ctime)
 
mTime = time.strftime('%Y-%m-%d %H:%M:%S', modifiedTime)
cTime = time.strftime('%Y-%m-%d %H:%M:%S', createdTime)
 
print("modifiedTime " + mTime)
print("createdTime " + cTime)