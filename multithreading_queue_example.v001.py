import os
import threading
from queue import Queue
import time
import sys
import timeit

path = "C:\\Users\\rmacaluso\\Desktop\\test_data"
filename = "test"
threads_num = os.cpu_count()
lock = threading.Lock()
time_between_reports = 1
time_between_checks = 1

def create_file(file_path):
    with open(file_path, 'w+') as f:
        num_chars = 5000000
        f.write('0' * num_chars)
    return file_path

def thread_handler():
    while True:
        task = q.get()
        create_file(task)
        q.task_done()
        if q.empty():
            break

def report_progress_until_finished(q):
    qsize_init = q.qsize()
    print ("%s\n" % (qsize_init))
    while not q.empty():
        portion_finished = 1 - (q.qsize() / qsize_init)
        print("Qsize: %d\n" % (q.qsize()))
        if q.empty():
            portion_finished = 1
        print("run_parallel: {:.1%} jobs are finished".format(portion_finished))


thread_list = []
print ("Starting\n")
print ("Thread_num: %d\n" % (threads_num))
maxfiles = 10000

q = Queue()
for x in range(threads_num):
    t = threading.Thread(target = thread_handler, name = "thread_%03d" % (x))
    # this ensures the thread will die when the main thread dies
    # can set t.daemon to False if you want it to keep running
    #t.daemon = True
    print ("starting thread\n")
    t.start()
    thread_list.append(t)

for i in range(0, int(maxfiles)):
    file_out_name = "%s.%04d.txt" % (filename, i)
    file_path = os.path.join(path,file_out_name)
    q.put(file_path)

report_progress_until_finished(q)

for t in thread_list:
    t.join()

print ("All Threads Complete")
