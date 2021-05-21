# coding=utf-8
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify,send_from_directory
from pyfiles.WEBrank import webUpRank,webVideoRank
import json
app = Flask(__name__)

@app.route('/uploaderRanking', methods = ['POST','GET'])
def uploaderRanking():
    uplist = webUpRank()
    return render_template('uploaderRanking.html', uplist = json.dumps(uplist,default = lambda x: x.__dict__,indent=4))
    
@app.route('/reUpRank', methods = ['POST','GET'])
def reUpRank():
    #todo: refresh
    uplist = webUpRank()
    return render_template('uploaderRanking.html', uplist = json.dumps(uplist,default = lambda x: x.__dict__,indent=4))

@app.route('/videoRanking', methods = ['POST','GET'])
def videoRanking():
    vlist,field = webVideoRank()
    return render_template('videoRanking.html',vlist = json.dumps(vlist,default = lambda x:x__dict__,indent=4),field=field)

@app.route('/reVideoRank', methods = ['POST','GET'])
def reVideoRank():
    #todo:refresh
    vlist,field = webVideoRank()
    return render_template('videoRanking.html',vlist = json.dumps(vlist,default = lambda x:x__dict__,indent=4),field=field)
 
@app.route('/uploaderRelation', methods = ['POST','GET'])
def uploaderRelation():
    return render_template('uploaderRelationship.html')

@app.route('/videoAnalysis', methods = ['POST','GET'])
def videoAnalysis():
    return render_template('individualAnalysis.html')

@app.route('/uploaderAnalysis', methods = ['POST','GET'])
def uploaderAnalysis():
    return render_template('individualAnalysis.html')

@app.route('/summary', methods = ['POST','GET'])
def summary():
    return send_from_directory('static','summary.pdf')


    
@app.route('/', methods=['POST', 'GET']) 

@app.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1129, debug=True)
