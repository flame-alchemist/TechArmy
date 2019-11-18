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


app=Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

client = pymongo.MongoClient("mongodb+srv://rohansharma1606:_kwB&9Q4GTZg2fA@se-6kdpi.mongodb.net/test?retryWrites=true&w=majority")
db = client.hack_se
fs = gridfs.GridFS(db)

# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
#     response.headers.add('Origin', '127.0.0.1')
#     return response

# <--------------------------ADD STUDENT----------------->
@app.route("/api/v1/student", methods=['POST'])
def addStudent():
    student = db.student
    name = request.json["name"]
    rollno = request.json["rollno"]
    email = request.json["email"]
    phno = request.json["phno"]
    university = request.json["university"]
    cgpa = request.json["CGPA"]

    res = student.find_one({'email':email})

    if res:
        abort(405)
    else:
        student.insert({"name":name, "rollno":rollno, "_id":email, "phno":phno, "university":university, "CGPA":cgpa})

        return jsonify({}),201

# <--------------------------ADD USER----------------->
@app.route('/addUser',methods= ['POST','OPTIONS'])
def addUser():
	if request.method == 'POST':
		user = db.user
		
		email = request.json["email"]
		name = request.json["name"]
		organization = request.json["organization"]
		password = request.json["password"]
		password = base64.b64encode(password.encode("utf-8"))
		
		res = user.find_one({"_id":email})
		if res:
			abort(405)
		else:
			user.insert({"name":name, "_id":email, "organization":organization, "password":password})
			return jsonify({}),201
		client.close()
		
	else:
		return jsonify({}),405

# <--------------------------LOGIN USER----------------->
@app.route('/checkUser', methods=['POST'])
def checkUser():
	if request.method == 'POST':
		user = db.user
		
		email = request.json["email"]
		password = request.json["password"]
		password = base64.b64encode(password.encode("utf-8"))

		res = user.find_one({"_id":email, "password":password})
		if res:
			print('success')
			return jsonify({"email":res["_id"],"name":res["name"]}),201
		else:
			print('failure')
			return jsonify({}),403

# <--------------------------ADD PROBLEM----------------->
@app.route('/upload',methods=['POST'])
def addProblem():
    # f = request.files['file']
    # f.save(secure_filename(f.filename))
    # print(request.form)
    # print(request.files)
	problem = db.problem
    
	test_cases={}
	for i in range(len(request.files)//2):
		input_id = fs.put(request.files['input'+str(i)])
		output_id = fs.put(request.files['output'+str(i)])
		print(type(input_id),input_id)
		temp = {"input_file":input_id, "output_file":output_id, "score":request.form['score'+str(i)]}
		test_cases["test_case_no_"+str(i)]=temp 
	problem_id = str(uuid.uuid1())
	problem_upload = {"problem_id":problem_id,"problem_title":request.form['problem_title'], "problem_description":request.form['problem_description'], 
                "sample_input":request.form['sample_input'], "sample_output":request.form['sample_output'], 
                "max_time_limit":request.form['max_time_limit'], "Test_cases":test_cases}
    
	print(problem_upload)
	problem.insert_one(problem_upload)
	client.close()

	return jsonify({"id":problem_id}),200

# <--------------------------ADD CONTEST----------------->
@app.route('/addContest', methods = ['POST'])
def addContest():
	contest_upload = request.json

	contest = db.contest
	res = contest.insert_one(contest_upload)	
	if res:
		return jsonify({}),201
	else:
		return jsonify({}),405

# <--------------------------VIEW CONTEST----------------->
@app.route('/viewContest', methods = ['POST'])
def viewContest():
	contest_upload = request.json

	contest = db.contest
	res = contest.insert_one(contest_upload)
	if res:
		return jsonify({}),201
	else:
		return jsonify({}),405
# @app.route('/addContest',methods = ['POST','OPTIONS'])
# def addContest():
# 	if request.method == 'POST':
# 		post = request.json
# 		posts = db.contest
# 		posts1 = db.problem
# 		posts2 = db.user
# 		pid = post["problem_id"]
# 		em = post["user"] 
# 		if (posts1.find({"problem_id":pid}) is not None) and (posts2.find({"email":em}) is not None):
# 			post_id=posts.insert_one(post)
# 			return "added"
# 		else:
# 			return "not added"
			
# 		client.close()
# 	else:
# 		return jsonify({}),405

'''
@app.route('/upload',methods=['POST','OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def uploaded():
	if request.method == 'POST':
		f=request.files['file'].filename
		client = pymongo.MongoClient("mongodb+srv://rohansharma1606:_kwB&9Q4GTZg2fA@se-6kdpi.mongodb.net/test?retryWrites=true&w=majority")
		db=client.gridfs_example
		fs=gridfs.GridFS(db)
		a=fs.put(f)
		return a,200
'''		
	
		
@app.route('/getProblemDescription',methods= ['GET','OPTIONS'])
def getProblemDescription():
		if request.method == 'GET':
			pid=request.args.get('problem_id',type=str)
			ab=db.problem.find_one({"problem_id":pid})
			ab1=json.loads(json_util.dumps(ab))
			return ab1,201
		else:
			return jsonify({}),405

@app.route('/getTestCases',methods= ['GET','OPTIONS'])
def getTestCases():
		print(request.json)
		print(request.args)
		if request.method == 'GET':
			# pid=request.args.get('problem_id',type=str)
			pid = request.json['problem_id']
			print("pid",pid)
			ab=db.problem.find_one({"problem_id":pid})
			ab1 = json.loads(json_util.dumps(ab))
			cd=ab1["Test_cases"]
			#print(cd['test_case_no_0']['input_file'])
			#print(cd['test_case_no_1']['input_file'])
			test_cases = {}
			for key,value in cd.items():
				temp = {
					'input_file' : fs.get(ObjectId(cd[key]['input_file']['$oid'])).read().decode('ascii'),
					'output_file' : fs.get(ObjectId(cd[key]['output_file']['$oid'])).read().decode('ascii'),
					'score' : cd['test_case_no_0']['score']
				}
				test_cases[key[-1]] = temp
			print(test_cases)
			# content = fs.get(ObjectId(cd['test_case_no_0']['input_file']['$oid'])).read()
			# print(content)
			return jsonify(test_cases),200
		else:
			return jsonify({}),405

@app.route('/getBestScore',methods= ['GET','OPTIONS'])
def getBestScore():
		if request.method == 'GET':
			pid=request.args.get('Contest_id',type=str)
			sid=request.args.get('Student_id',type=str)
			ab=db.contest.find_one({"Contest_id":pid})
			ab1 = json.loads(json_util.dumps(ab))
			cd=ab1["Student_list"]
			for key,val in cd.items():
				if key==sid:
					return val["Best_score"]
		else:
			return jsonify({}),405

'''@app.route('/addBestCode',methods= ['PUT','OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def addBestCode():
		if request.method == 'PUT':
			client = pymongo.MongoClient("mongodb+srv://rohansharma1606:_kwB&9Q4GTZg2fA@se-6kdpi.mongodb.net/test?retryWrites=true&w=majority")
			db=client.hack_se
			post=request.json
			cid=post["Contest_id"]
			sid=post["Student_id"]
			ns=post["Best_score"]
			bc=post["Best_code"]
			bcl=post["Best_code_language"]
			ab=db.contest.find_one({"Contest_id":cid})
			ab1 = json.loads(json_util.dumps(ab))
			cd=ab1["Student_list"]
			new_val={}
			n_val={}
			for key,val in cd.items():
				if key==sid and ns>val["Best_score"]:
					new_val={"Student_id":sid,"Best_code":bc,"Best_score":ns,"Best_code_language":bcl}
                    old_val=val
			dict={"$set":new_val}
			myco=db.contest["Student_list"]
			mycol=myco[sid]
			
			
			
			db=db.contest
			
		else:
			return jsonify({}),405'''

if __name__ == '__main__':
	app.run(port=5001,debug=True)