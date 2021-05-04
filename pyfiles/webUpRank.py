import requests
import time, random
from datetime import datetime
from pyfiles.MysqlConnect import MysqlConnect
from pyfiles.Spider import Spider

def webUpRank():
    mysqlconnect = MysqlConnect()
    sql = "SELECT `ID`,`Followings`,`Rank` from `NewestTop100` ORDER BY `Rank`;"
    upList = [(ID, Followings, Rank) for (ID, Followings, Rank,) in mysqlconnect.queryOutCome(sql)]
    return upList