from pyfiles.WEBvideo import Video
def videoAna(bid):
    v = Video()
    v.bvid = bid
    v.start_crawlling()
    vs=[]
    vs.append(v)
    #v.printInfo()
    return vs