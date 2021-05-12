# coding=utf-8
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from pyfiles.webUpRank import webUpRank
import json
app = Flask(__name__)

@app.route('/uploaderRanking', methods = ['POST','GET'])
def uploaderRanking():
    uplist = webUpRank()
    return render_template('uploaderRanking.html', upList = json.dumps(uplist))
    
@app.route('/uploaderRelation', methods = ['POST','GET'])
def uploaderRelation():
    return render_template('uploaderRelationship.html')
'''
@app.route('/individualAnalysis', methods = ['POST','GET'])
def individualAnalysis():
    return render_template('individualAnalysis.html')
'''
@app.route('/videoAnalysis', methods = ['POST','GET'])
def videoAnalysis():
    return render_template('individualAnalysis.html')

@app.route('/uploaderAnalysis', methods = ['POST','GET'])
def uploaderAnalysis():
    return render_template('individualAnalysis.html')

@app.route('/summary', methods = ['POST','GET'])
def summary():
    return render_template('summary.html')

@app.route('/videoRanking', methods = ['POST','GET'])
def videoRanking():
    return render_template('videoRanking.html')
    
@app.route('/', methods=['POST', 'GET']) 

@app.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1129, debug=True)
