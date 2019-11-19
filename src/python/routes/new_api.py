import pymongo
import datetime
import json
from flask import Flask, render_template, request, url_for, redirect, abort, jsonify, make_response
from flask_cors import CORS, cross_origin
from bson import json_util
from bson.json_util import dumps
import random
import gridfs

app=Flask(__name__)

@app.route('/getContestID',methods= ['GET','OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getContestID():
	if request.method == 'GET':
			client = pymongo.MongoClient("mongodb+srv://rohansharma1606:_kwB&9Q4GTZg2fA@se-6kdpi.mongodb.net/test?retryWrites=true&w=majority")
			db=client.hack_se
			posts = db.contest
			uid=request.args.get('User',type=str)
			ab=posts.find({"user":uid})
			data=list(ab)
			#print(data)
			c=0
			abc={}
			for i in data:
				abc[c]=i
				c=c+1
			di=json.loads(json_util.dumps(abc))
			return jsonify({"LIST":di}),201




@app.route('/getReport',methods= ['GET','OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getReport():
	if request.method == 'GET':
			client = pymongo.MongoClient("mongodb+srv://rohansharma1606:_kwB&9Q4GTZg2fA@se-6kdpi.mongodb.net/test?retryWrites=true&w=majority")
			db=client.hack_se
			posts = db.contest
			uid=request.args.get('User',type=str)
			cid=request.args.get('Contest_id',type=str)
			ab=posts.find({"user":uid,"Contest_id":cid},{"_id":0,"Student_list":1})
			data=list(ab)
			return jsonify({"LIST":data}),201



if __name__ == '__main__':
	app.run(debug=True)
