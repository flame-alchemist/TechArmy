from multiprocessing.pool import ThreadPool
from lang import languages
from flask import Flask, jsonify, request
import os
from subprocess import run, PIPE, check_output
import time
from subprocess import Popen, PIPE
import time
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool
import os
import signal
import requests
import json
import pickle
app = Flask(__name__)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET, PUT, POST,DELETE,OPTIONS')
    response.headers.add('Origin', '127.0.0.1')
    return response


def threading(p):
    fp = open("in0"+str(p)+".txt", "r")
    contents = fp.read()
    fp.close()

    import signal

    def signal_handler(signum, frame):
        raise Exception("Timed out!")

    timeout = False
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(2)   # timeout seconds
    try:
        start_time = time.time()
        op = Popen(["python", "temp.py"], stdin=PIPE,
                   stdout=PIPE, stderr=PIPE)
        stdout, stderr = op.communicate(contents.encode("utf-8"))
        t = (time.time() - start_time)
        stdout = stdout.decode()
        stderr = stderr.decode()
    except Exception as i:
        print(i.args[0])
        timeout = True
        return(timeout)

    return(stdout, stderr, t, timeout)
    # write code to compare output with test_case_op file and update value of status

def populate_problem(pid):
    r = requests.get('http://0.0.0.0:5000/getTestCases', data=json.dumps({'problem_id':pid}),
                  headers={'Content-Type': 'application/json'})
    print('r-json',r)
    os.makedirs("problems/"+pid)
    score = {}
    path = 'problems/'+pid+'/'
    for key,value in r.json().items():
        fp = open(path+'in'+key+'.txt','w')
        fp.write(value['input_file'])
        fp.close()
        fp = open(path+'op'+key+'.txt','w')
        fp.write(value['output_file'])
        fp.close()
        score[key]=value["score"]
    fp = open(path+'score.p','wb')
    pickle.dump(score,fp)
    fp.close()
    fp = open(path+'number_cases.txt','w')
    fp.write(str(len(r.json())))
    fp.close()


@app.route('/v1/run_code', methods=['POST'])
def compile():
    # recieve contest_id
    # problem_id recieved, populate problem id by making a call to db if folder doesnt exist
    print(request)
    # code = ("print(\"hello\")")
    # language = "py"
    try:
        # make dir for each student under each contest
        os.makedirs(request.json['contest_id'] +
                    "/temp_"+request.json['student_id'])
            
    except:
        pass

    if(os.path.isdir("problems/"+request.json["problem_id"]) == False):
        populate_problem(request.json['problem_id'])


    # store the given code into the student folder
    fp = open(request.json['contest_id']+"/temp_" +
              request.json['student_id']+"/temp."+request.json['language'], "w")
    fp.write(request.json['code'])
    fp.close()

    # call languages class and get status(coorect/wrong answer) or if error occured
    lang = languages(
        request.json['student_id'], request.json['problem_id'], request.json['contest_id'], request.json['time_out'])
    ip_lang = request.json['language']
    if(ip_lang == "py"):
        status, err = lang.py_lang()
    elif(ip_lang == "c"):
        status, err = lang.C_lang()
    elif(ip_lang == "cpp"):
        status, err = lang.Cpp_lang()
    elif(ip_lang == "java"):
        status, err = lang.java_lang()

    path = 'problems/'+request.json["problem_id"]+'/'

    scores = pickle.load(open(path+'score.p','rb'))
    print(scores)
    total_score = 0
    if err:
        for i in range(len(status)):
            if status[i][0]:
                total_score+=int(scores[str(i)])
    
    r = requests.post('http://0.0.0.0:5000/addBestCode', data=json.dumps({'contest_id':request.json['contest_id'],
                                                                            'student_id':request.json['student_id'],
                                                                            'score':total_score,
                                                                            'code':request.json['code'],
                                                                            'language':request.json['language']}),headers={'Content-Type': 'application/json'})




    # new_gui = subprocess.Popen(["python", path])
    # keyboard_output = subprocess.check_output(["./a.out <", path[:1],path[2:]]).decode("utf-8")
    # print(keyboard_output)
    # keyboard_output = keyboard_output[:-1]
    # keyboard_output.decode("utf-8")
    # print(keyboard_output)

    # questions = obj.extract_questions(request.json)
    # # {'questions':obj.test_transcript(request.json['transcript'])}
    #print('app process id ', os.getpid())
    return jsonify(status), 200


@app.route('/v1/test', methods=['POST'])
def compile_test():
    # recieve contest_id
    # problem_id recieved, populate problem id by making a call to db if folder doesnt exist
    print(request)
    # code = ("print(\"hello\")")
    # language = "py"

    # store the given code into the student folder
    fp = open("temp."+request.json['language'], "w")
    fp.write(request.json['code'])
    fp.close()

    p = Pool(processes=5)
    results = p.map(threading, list(range(5)))
    # print('debug 1', p)

    p.close()

    # keyboard_output = keyboard_output[:-1]
    # keyboard_output.decode("utf-8")
    # print(keyboard_output)

    # questions = obj.extract_questions(request.json)
    # # {'questions':obj.test_transcript(request.json['transcript'])}

    return jsonify(results), 200


if __name__ == '__main__':

    app.run(host = '0.0.0.0',port=5000, debug=True)
