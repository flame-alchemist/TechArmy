import pymongo
import datetime
import json
from flask import Flask, render_template, request, url_for, redirect, abort, jsonify, make_response
from flask_cors import CORS, cross_origin
from bson import json_util
from bson.json_util import dumps,ObjectId
import random
import gridfs,base64
import uuid
import requests
import json

app=Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/getTestCases", methods=['GET'])
def getTestCases():
    r = requests.get('http://localhost:5001/getTestCases', data=request.data,
                  headers={'Content-Type': 'application/json'})
    
    if(r.status_code==200):
        return r.json(),200
    else:
        return {},400




@app.route('/getProblemDescription',methods= ['POST'])
def getProblemDescription():
    r = requests.post('http://localhost:5001/getProblemDescription',data=request.data,headers={'Content-Type': 'application/json'})
    return r.json(),r.status_code


@app.route("/addStudent", methods=['POST'])
def addStudent():
    r = requests.post('http://localhost:5001/addStudent',data=request.data,headers={'Content-Type': 'application/json'})

    
    if(r.status_code==201):
        return r.json(),201
    else:
        return {},400

@app.route('/checkUser', methods=['POST'])
def checkUser():
    r = requests.post('http://localhost:5001/checkUser',data=request.data,headers={'Content-Type': 'application/json'})

    
    if(r.status_code==201):
        return r.json(),201
    else:
        return {},400


@app.route('/upload',methods=['POST'])
def addProblem():
    r = requests.post('http://localhost:5001/upload',data=request.data,files=request.files)

    if(r.status_code==200):
        return r.json(),200
    else:
        return {},400

@app.route('/addContest', methods = ['POST'])
def addContest():
    r = requests.post('http://localhost:5001/addContest',data=request.data,headers={'Content-Type': 'application/json'})

    
    if(r.status_code==201):
        return r.json(),201
    else:
        return {},400

@app.route('/addUser',methods= ['POST','OPTIONS'])
def addUser():
    r = requests.post('http://localhost:5001/addUser',data=request.data,headers={'Content-Type': 'application/json'})
    return r.json(),r.status_code

@app.route('/getContest', methods = ['POST'])
def getContest():
    r = requests.post('http://localhost:5001/getContest',data=request.data,headers={'Content-Type': 'application/json'})
    return r.json(),r.status_code

@app.route('/addBestCode',methods= ['POST'])
def addBestCode():
    r = requests.post('http://localhost:5001/addBestCode',data=request.data,headers={'Content-Type': 'application/json'})
    return r.json(),r.status_code

@app.route('/checkStatus',methods= ['POST'])
def checkStatus():
    r = requests.post('http://localhost:5001/checkStatus',data=request.data,headers={'Content-Type': 'application/json'})
    return r.json(),r.status_code

@app.route('/v1/run_code', methods=['POST'])
def compile():
    r = requests.post('http://localhost:5002/v1/run_code',data=request.data,headers={'Content-Type': 'application/json'})
    print(r)
    return jsonify(r.json()),r.status_code

@app.route('/endTest',methods= ['POST'])
def endTest():
    r = requests.post('http://localhost:5001/endTest',data=request.data,headers={'Content-Type': 'application/json'})
    return r.json(),r.status_code

if __name__ == '__main__':
	app.run(port=5000,debug=True)