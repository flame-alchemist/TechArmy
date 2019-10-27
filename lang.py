from subprocess import Popen, PIPE
import time
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool
import os
import signal

#   Getting JAVA class name
def get_class_name(program_path):
    fptr = open(program_path+'.java',"r")
    contents = tuple(fptr)
    fptr.close()

    contents =[x.strip()  for x in contents]

    for lines in contents:
        words = []
        if 'class' in lines:
            words = lines.split(' ')
            for i in range(len(words)):
                if words[i] == 'class':
                    return words[i+1]
            break


class languages:

    def __init__(self, student_id, problem_id, contest_id, time_out):
        self.student_id = student_id
        self.problem_id = problem_id
        self.contest_id = contest_id
        self.student_path = contest_id+"/temp_"+student_id
        self.code_path = self.student_path+"/temp"
        self.time_out = time_out
        self.class_name = ''

    def get_number_of_testcases(self):
        fp = open("problems/"+self.problem_id+"/number_cases.txt", "r")
        contents = fp.read()
        return (int(contents))

    def processes_py(self, p):
        code_path = self.code_path+".py"
        pid = os.getpid()
        fp = open("problems/"+self.problem_id+"/in"+str(p)+".txt", "r")
        contents = fp.read()
        fp.close()

        start_time = time.time()
        op = Popen(["timeout", "2s", "python", code_path], stdin=PIPE,
                   stdout=PIPE, stderr=PIPE)
        stdout, stderr = op.communicate(contents.encode("utf-8"))
        t = (time.time() - start_time)
        stdout = stdout.decode().strip()
        stderr = stderr.decode()
        print(stdout, contents)
        if stdout == '':
            return  False,'','',"Time Limit Exceeded",0.0


        # write code to compare output with test_case_op file and update value of status
        fp = open("problems/"+self.problem_id+"/op"+str(p)+".txt", "r")
        contents = fp.read().strip()
        fp.close()
	
        status = (stdout == contents)

        return(status, stdout, contents, stderr, round(t,4))

    def py_lang(self):
        code_path = self.code_path+".py"

        # to check for compilation error; dont proceed into threading if compilation error
        #op = Popen(["python", code_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        #stdout, stderr = op.communicate()
        #stdout = stdout.decode()
        #stderr = stderr.decode()
        stderr = ''

        testcases = self.get_number_of_testcases()

        p = ThreadPool()
        results = p.map(self.processes_py, list(range(testcases)))
        p.close()

        '''{
            error: True,
            result: {
                [time, status]
            }
        }'''
        return results, 1

    def processes_C(self, p):

        fp = open("problems/"+self.problem_id+"/in"+str(p)+".txt", "r")
        contents = fp.read()
        fp.close()

        start_time = time.time()
        op = Popen(["timeout","2s",self.student_path+"/./a.out"],
                    stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = op.communicate(contents.encode("utf-8"))
        t = (time.time() - start_time)
        stdout = stdout.decode()
        stderr = stderr.decode()
        print(stdout, contents)
        if stdout == '':
            return  False,'','',"Time Limit Exceeded",0.0

        # write code to compare output with test_case_op file and update value of status
        fp = open("problems/"+self.problem_id+"/op"+str(p)+".txt", "r")
        contents = fp.read()
        fp.close()

        status = (stdout.strip() == contents.strip())

        return(status, stdout, contents, stderr, round(t,4))

    def C_lang(self):
        code_path = self.code_path+".c"

        op = Popen(["gcc", "-w", code_path,"-o", self.student_path+"/./a.out"],
                   stdin=PIPE, stdout=PIPE, stderr=PIPE)
        time.sleep(1)
        stdout, stderr = op.communicate()
        stdout = stdout.decode()
        stderr = stderr.decode()

        if(stderr == ''):
            testcases = self.get_number_of_testcases()

            p = Pool(processes=testcases)
            results = p.map(self.processes_C, list(range(testcases)))
            p.close()

            return results, 1

        else:

            return (False,'','',stderr,0.0), 0

    def processes_cpp(self, p):

        fp = open("problems/"+self.problem_id+"/in"+str(p)+".txt", "r")
        contents = fp.read()
        fp.close()

        start_time = time.time()
        op = Popen(["timeout","2s",self.student_path+"/./a.out"],
                    stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = op.communicate(contents.encode("utf-8"))
        t = (time.time() - start_time)
        stdout = stdout.decode()
        stderr = stderr.decode()
        print(stdout, contents)
        if stdout == '':
            return  False,'','',"Time Limit Exceeded",0.0


        # write code to compare output with test_case_op file and update value of status
        fp = open("problems/"+self.problem_id+"/op"+str(p)+".txt", "r")
        contents = fp.read()
        fp.close()

        status = (stdout.strip() == contents.strip())

        return(status, stdout, contents, stderr, round(t,4))

    def Cpp_lang(self):
        code_path = self.code_path+".cpp"

        op = Popen(["g++", code_path,"-o", self.student_path+"/./a.out"],
                   stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = op.communicate()
        stdout = stdout.decode()
        stderr = stderr.decode()

        if(stderr == ''):
            testcases = self.get_number_of_testcases()

            p = Pool(processes=testcases)
            results = p.map(self.processes_cpp, list(range(testcases)))
            p.close()

            return results, 1

        else:

            return (False,'','',stderr,0.0), 0

    def processes_java(self, p):

        fp = open("problems/"+self.problem_id+"/in"+str(p)+".txt", "r")
        contents = fp.read()
        fp.close()

        start_time = time.time()
        op = Popen(["timeout","2s","java","-cp",self.student_path,self.class_name],
                    stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = op.communicate(contents.encode("utf-8"))
        t = (time.time() - start_time)
        stdout = stdout.decode()
        stderr = stderr.decode()
        print(stdout, contents)
        if stdout == '':
            return  False,'','',"Time Limit Exceeded",0.0


        # write code to compare output with test_case_op file and update value of status
        fp = open("problems/"+self.problem_id+"/op"+str(p)+".txt", "r")
        contents = fp.read().strip()
        fp.close()
	
        status = (stdout.strip() == contents)

        return(status, stdout, contents, stderr, round(t,4))

    def java_lang(self):
        self.class_name = get_class_name(self.code_path)
        code_path = self.code_path[:-4]+self.class_name+".java"
        fp1 = open(code_path,"w")
        fp2 = open(self.code_path+".java","r")
        contents = fp2.read()
        fp1.write(contents)
        fp1.close()
        fp2.close()

        op = Popen(["javac", code_path],
                   stdin=PIPE, stdout=PIPE, stderr=PIPE)
        time.sleep(2)
        stdout, stderr = op.communicate()
        stdout = stdout.decode()
        stderr = stderr.decode()

        if(stderr == ''):
            testcases = self.get_number_of_testcases()

            p = Pool(processes=testcases)
            results = p.map(self.processes_java, list(range(testcases)))
            p.close()

            return results, 1

        else:

            return (False,'','',stderr,0.0), 0
