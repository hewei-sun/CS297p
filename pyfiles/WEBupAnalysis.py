from pyfiles.WEBuploader import Uploader

def uploaderAna(id):
    up = Uploader(id)
    up.crawl_basic()
    #up.crawl_videoList()
    ups = []
    ups.append(up)
    return ups