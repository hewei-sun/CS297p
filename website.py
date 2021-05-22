# coding=utf-8
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify,send_from_directory
from pyfiles.WEBrank import webUpRank,webVideoRank,wreUpRank,wreVideoRank
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

@app.route('/reUpRank/reUpRank', methods = ['POST','GET'])
def rereu():
    return redirect(url_for('reUpRank'))

@app.route('/reUpRank', methods = ['POST','GET'])
def reUpRank():
    uplist = wreUpRank()
    return render_template('uploaderRanking.html', uplist = json.dumps(uplist,default = lambda x: x.__dict__,indent=4))

@app.route('/videoRanking', methods = ['POST','GET'])
def videoRanking():
    vlist,field,start = webVideoRank()
    return render_template('videoRanking.html',vlist = json.dumps(vlist,default = lambda x:x__dict__,indent=4),field=field,start=start)

@app.route('/reVideoRank/reVideoRank/<fields>', methods = ['POST','GET'])
def rerev(fields):
    return redirect(url_for('reVideoRank',fields=fields))
    
@app.route('/reVideoRank/<fields>', methods = ['POST','GET'])
def reVideoRank(fields):
    if fields=="index":
        return redirect(url_for('index'))
    vlist,field,start = wreVideoRank(fields)
    return render_template('videoRanking.html',vlist = json.dumps(vlist,default = lambda x:x__dict__,indent=4),field=field,start=start)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1129, debug=True)
