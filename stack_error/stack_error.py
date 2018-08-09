from bs4 import BeautifulSoup
import requests
from subprocess import PIPE, Popen
import sys
import Queue
from threading import Thread

SO_BASE_URL = "https://stackoverflow.com"

def _get_stack_question(query):
    search_url = SO_BASE_URL + "/search?pagesize=50&q=%s" % query.replace(' ','+')
    search_resp = requests.get(url=search_url)
    search_soup = BeautifulSoup(search_resp.text,"html.parser")
    return search_soup.find_all('a',{"class": "question-hyperlink"})[0]['href']


def _get_all_answers(question_href):
    url = SO_BASE_URL + "/" + question_href
    resp = requests.get(url=url)
    soup = BeautifulSoup(resp.text, "html.parser")
    print '********************************************'
    for answer in soup.find_all("div", {"class": "post-text"})[1:]:
        print answer.get_text()
        print '********************************************'


def read(pipe, funcs):
    for line in iter(pipe.readline, b''):
        for func in funcs:
            func(line.decode("utf-8"))
    pipe.close()


def write(get):
    for line in iter(get, None):
        sys.stdout.write(line)


def _compile_python(cmd):
    process = Popen(cmd,close_fds=True,stdout=PIPE,stderr=PIPE,bufsize=1,shell=True)
    q = Queue.Queue()
    op,error=[],[]

    thread_stdout = Thread(target=read,args=(process.stdout,[q.put,op.append]))
    thread_stderr = Thread(target=read,args=(process.stderr,[q.put,op.append]))
    thread_write = Thread(target=write,args=(q.get,))

    for t in (thread_stderr,thread_stdout,thread_write):
        t.daemon = True
        t.start()

    for t in (thread_stdout,thread_stderr):
        t.join()

    q.put(None)

    op = ' '.join(op)
    error = ' '.join(error)
    return (op,error)


def _get_query_string(op):
    return "python " + op.split('\n')[-2][1:]


def main():
    # query ="ImportError: No module named queue"
    # _get_all_answers(str(_get_stack_question(query)))

    file_name = "test.py"
    cmd = "python test.py"

    # file_name = sys.argv[1]

    # validate file extention
    # file_ext = file_name.split(".")[-1] == "py"
    # if not file_ext:
    #     print "Only python files are supported"
    #
    # cmd = "python " + file_name

    op, error = _compile_python(cmd=cmd)
    query = _get_query_string(op)
    _get_all_answers(str(_get_stack_question(query)))



if __name__ == '__main__':
    '''
        Task 1: Use subprocess to run python command inside this and get the error (Should use threads to stderr and stdout)
        Task 2: Parse the stderr and generate the query string
        Task 3: Search so and find is there any corresponding question for the query
        Task 4: Get all the answers for the question from so
        Additional Tasks:
        Task 5: if syntax error go back to stack trace and try to find the cause
        Task 6: crete pip module
        #TODO still thinking
    '''

    # query ="ImportError: No module named queue"
    # _get_all_answers(str(_get_stack_question(query)))

    file_name="test.py"
    cmd="python test.py"

    # file_name = sys.argv[1]

    #validate file extention
    # file_ext = file_name.split(".")[-1] == "py"
    # if not file_ext:
    #     print "Only python files are supported"
    #
    # cmd = "python " + file_name

    op,error = _compile_python(cmd=cmd)
    query = _get_query_string(op)
    _get_all_answers(str(_get_stack_question(query)))