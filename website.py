# coding=utf-8
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify,send_from_directory
from pyfiles.WEBrank import webUpRank,webVideoRank,wreVideoRank
from pyfiles.WEBrefresh import refreshUpRank
from pyfiles.WEBupAnalysis import uploaderAna
from pyfiles.WEBmenu import upMe,viMe,rankMe
from pyfiles.WEBsingleQueries import searchUp,searchVideo
from pyfiles.WEBvideoAnalysis import videoAna
from pyfiles.WEBrelation import showRelation
import json
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET']) 

@app.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

#--------up ranking---------
@app.route('/uploaderRanking/<page>', methods = ['POST','GET'])
def uploaderRanking(page):
    uplist = webUpRank()
    return render_template('uploaderRanking.html', uplist = json.dumps(uplist,default = lambda x: x.__dict__,indent=4),page=page)

@app.route('/reUpRank', methods = ['POST','GET'])
def reUpRank():
    refreshUpRank()
    return redirect(url_for('uploaderRanking',page='1'))

#----------video ranking---------
@app.route('/videoRank/<field>/<page>', methods = ['POST','GET'])
def videoRank(field,page):
    vlist = webVideoRank(field)
    return render_template('videoRankingf.html',vlist = json.dumps(vlist,default = lambda x:x.__dict__,indent=4),field=field,page = page)

@app.route('/videoRanking', methods = ['POST','GET'])
def videoRanking():
    if request.method == 'POST':
        field = request.form.get('bid')
        return redirect(url_for('videoRank',field=field,page = '1'))
    return render_template('videoR.html')

@app.route('/reVideoRank/<field>', methods = ['POST','GET'])
def reVideoRank(field):
    #print(fields)
    wreVideoRank(field)
    return redirect(url_for('videoRank',field=field,page='1'))

@app.route('/rankM',methods = ['POST','GET'])
def rankM():
    field = rankMe()
    return jsonify({"success": 200, "msg": "success", "field": field})

#----------up analysis-------------
@app.route('/uploaderAnalysis', methods = ['POST','GET'])
def uploaderAnalysis():
    if request.method == 'POST':
        #print(request.form)
        upid = request.form.get('upid')
        if upid == "":
            up = request.form.get('text')
            if up == "":
                return render_template('uploaderAnalysis.html')
            name = request.form.get('idname')
            if name == '1':
                upid = searchUp(up)
            else:
                upid = up
        #print(upid)
        return redirect(url_for('uploaderA',upid = upid))
    return render_template('uploaderAnalysis.html')
 
@app.route('/upMenu', methods = ['POST','GET'])   
def upMenu():
    uplist = upMe()
    return jsonify({"success": 200, "msg": "success", "uplist": uplist})

@app.route('/uploaderA/<upid>', methods = ['POST','GET'])
def uploaderA(upid):
    if upid == "index":
        return redirect(url_for('index'))
    if request.method == 'POST':
        upid = request.form.get('upid')
        if upid == "":
            up = request.form.get('text')
            if up == "":
                return redirect(url_for('uploaderAnalysis'))
            name = request.form.get('idname')
            if name == '1':
                upid = searchUp(up)
            else:
                upid = up
        return redirect(url_for('uploaderA',upid = upid))
    up,rank,infos = uploaderAna(upid)
    return render_template('uploaderA.html',up = json.dumps(up,default = lambda x:x.__dict__,indent=4,separators=(',',':')),rank = rank,infos = json.dumps(infos,default = lambda x:x.__dict__,indent=4))

@app.route('/summary', methods = ['POST','GET'])
def summary():
    return send_from_directory('static','summary.pdf')
    
#---------------video analysis-------------
@app.route('/videoAnalysis', methods = ['POST','GET'])
def videoAnalysis():
    if request.method == 'POST':
        print(request.form)
        bid = request.form.get('bid')
        if bid == "":
            vi = request.form.get('text')
            if vi == "":
                return render_template('videoAnalysis.html')
            name = request.form.get('idname')
            if name == '1':
                bid = searchVideo(vi)
            else:
                bid = vi
        return redirect(url_for('videoA',bid = bid))
    return render_template('videoAnalysis.html')
 
@app.route('/viMenu', methods = ['POST','GET'])   
def viMenu():
    vlist = viMe()
    return jsonify({"success": 200, "msg": "success", "vlist": vlist})

@app.route('/videoA/<bid>', methods = ['POST','GET'])
def videoA(bid):
    if bid == "index":
        return redirect(url_for('index'))
    if request.method == 'POST':
        print(request.form)
        bid = request.form.get('bid')
        if bid == "":
            vi = request.form.get('text')
            if vi == "":
                return redirect(url_for('videoAnalysis'))
            name = request.form.get('idname')
            if name == '1':
                bid = searchVideo(vi)
            else:
                bid = vi
        print(bid)
        return redirect(url_for('videoA',bid = bid))
    videos = videoAna(bid)
    return render_template('videoA.html',videos = json.dumps(videos,default = lambda x:x.__dict__,indent=4,separators=(',',':')))    
    
#---------------up relationship------------
@app.route('/uploaderRelation', methods = ['POST','GET'])
def uploaderRelation():
    relation,ups = showRelation()
    return render_template('uploaderRelationship.html',relations=json.dumps(relation,default=lambda x:x.__dict__,indent=4),ups = json.dumps(ups,default=lambda x:x.__dict__,indent=4))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1129, debug=True)
    #app.run(host='0.0.0.0', port=1129)
