# coding=utf-8
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify,send_from_directory
from pyfiles.WEBrank import webUpRank,webVideoRank
from pyfiles.WEBrefresh import refreshUpRank,refreshVideoRank
from pyfiles.WEBupAnalysis import uploaderAna
from pyfiles.WEBmenu import upMe
import json
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET']) 

@app.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/uploaderRanking', methods = ['POST','GET'])
def uploaderRanking():
    uplist = webUpRank()
    return render_template('uploaderRanking.html', uplist = json.dumps(uplist,default = lambda x: x.__dict__,indent=4))

@app.route('/reUpRank', methods = ['POST','GET'])
def reUpRank():
    refreshUpRank()
    return redirect(url_for('uploaderRanking'))

@app.route('/videoRanking/<fields>', methods = ['POST','GET'])
def videoRanking(fields):
    if fields == "index":
        return redirect(url_for('index'))
    if fields[0:10] == "uploaderA/":
        return redirect(url_for('fields'))
    vlist,field,start = webVideoRank()
    if fields =="init":
        fields = start
    return render_template('videoRanking.html',vlist = json.dumps(vlist,default = lambda x:x.__dict__,indent=4),field=field,start=fields)

@app.route('/videoRanking/uploaderA/<upid>',methods = ['POST','GET'])
def upRanktoAna(upid):
    return redirect(url_for('uploaderA',upid = upid))

@app.route('/videoRanking/reVideoRank/<fields>', methods = ['POST','GET'])
def reVideoRank(fields):
    refreshVideoRank(fields)
    return redirect(url_for('videoRanking',fields = fields))

@app.route('/uploaderAnalysis', methods = ['POST','GET'])
def uploaderAnalysis():
    if request.method == 'POST':
        upid = request.form.get('upid')
        if upid == "":
            name = request.form.get('idname')
            if name == '1':
                #todo:
                print("need convert")
            else:
                upid = req.form.get('name')
        return redirect(url_for('uploaderA',upid = upid))
    return render_template('uploaderAnalysis.html')
 
@app.route('/upMenu', methods = ['POST','GET'])   
def upMenu():
    uplist = upMe()
    print(uplist)
    return jsonify({"success": 200, "msg": "success", "uplist": uplist})

@app.route('/uploaderA/<upid>', methods = ['POST','GET'])
def uploaderA(upid):
    if upid == "index":
        return redirect(url_for('index'))
    if request.method == 'POST':
        upid = request.form.get('upid')
        return redirect(url_for('uploaderA',upid = upid))
    up = uploaderAna(upid)
    return render_template('uploaderA.html',up = json.dumps(up,default = lambda x:x.__dict__,indent=4,separators=(',',':')))

@app.route('/summary', methods = ['POST','GET'])
def summary():
    return send_from_directory('static','summary.pdf')
    

@app.route('/videoAnalysis', methods = ['POST','GET'])
def videoAnalysis():
    return render_template('individualAnalysis.html')

@app.route('/uploaderRelation', methods = ['POST','GET'])
def uploaderRelation():
    return render_template('uploaderRelationship.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1129, debug=True)
    #app.run(host='0.0.0.0', port=1129)
