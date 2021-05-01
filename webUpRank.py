import requests
import time, random
from datetime import datetime
from CS297p.MysqlConnect import MysqlConnect
from CS297p.Spider import Spider

def webUpRank():
    mysqlconnect = MysqlConnect()
    mysqlconnect.getConnect()
    sql = "SELECT `ID`,`Followings`,`Rank` from `NewestTop100` ORDER BY `Rank`;"
    upList = [(ID, Followings, Rank) for (ID, Followings, Rank,) in mysqlconnect.queryOutCome(sql)]
    return upList