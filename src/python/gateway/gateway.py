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
import os
import threading,time
from subprocess import call

app=Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


# ports=[5002,5003,5004]
container_dictionary = {}
no_of_requests = 0
port_count = 0
max_containers = 10
min_containers = 1

# container_dictionary[5002] = os.popen("sudo docker run -d -it --publish 5002:5000 -v /home/ubuntu/TechArmy/src/python/routes:/src/  test-cont").read().rstrip()



def start_last_container():
    global container_dictionary
    print('scaling up')
    max_cont_id = max(list(container_dictionary.keys()))
    container_id = os.popen("sudo docker run -d -it --publish " + str(max_cont_id + 1) + ":5000 -v /home/ubuntu/TechArmy/src/python/routes:/src/  test-cont").read().rstrip()
    container_dictionary[max_cont_id + 1] = container_id

def kill_last_container():
    global container_dictionary
    print('scaling down')
    max_cont_id = max(list(container_dictionary.keys()))
    cont_id_kill = container_dictionary[max_cont_id]
    tmp = os.popen("sudo docker container kill " + cont_id_kill).read()
    del(container_dictionary[max_cont_id])


def scale():
    global no_of_requests,container_dictionary
    print('scaling')
    if no_of_requests>10:
        #scale up
        if len(container_dictionary.keys())<10:
            start_last_container()
            time.sleep(1)
    elif no_of_requests<2:
        #scale down
        if len(container_dictionary.keys())>1:
            kill_last_container()
            time.sleep(1)
    no_of_requests = 0




class setInterval :
    def __init__(self,interval,action) :
        self.interval=interval
        self.action=action
        self.stopEvent=threading.Event()
        thread=threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self) :
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()) :
            nextTime+=self.interval
            self.action()

    def cancel(self) :
        self.stopEvent.set()

# start action every 0.6s
def start_services():
    global container_dictionary
    container_dictionary[5002] = os.popen("sudo docker run -d -it --publish 5002:5000 -v /home/ubuntu/TechArmy/src/python/routes:/src/  test-cont").read().rstrip()
    inter=setInterval(60,scale)




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

@app.route('/getReport',methods= ['POST'])
def getReposrt():
    r = requests.post('http://localhost:5001/getReport',data=request.data,headers={'Content-Type': 'application/json'})
    return r.json(),r.status_code    

@app.route('/v1/run_code', methods=['POST'])
def compile():
    global container_dictionary,no_of_requests,port_count
    r = requests.post('http://localhost:'+str(list(container_dictionary.keys())[port_count])+'/v1/run_code',data=request.data,headers={'Content-Type': 'application/json'})
    print(r)
    print(port_count)
    port_count = (port_count+1)%len(container_dictionary.keys())
    no_of_requests+=1
    return jsonify(r.json()),r.status_code

    


@app.route('/endTest',methods= ['POST'])
def endTest():
    r = requests.post('http://localhost:5001/endTest',data=request.data,headers={'Content-Type': 'application/json'})
    return r.json(),r.status_code

if __name__ == '__main__':
    start_services()
    app.run(host='0.0.0.0',port=5000,debug=True)
