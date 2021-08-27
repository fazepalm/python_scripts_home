import os
import threading
from queue import Queue
import time
import sys
import timeit
import shutil

root_path = "C:\\Users\\rmacaluso\\Desktop\\test_data"
filename = "test"
threads_num = os.cpu_count()
lock = threading.Lock()
time_between_reports = 1
time_between_checks = 1

def create_file(file_path):
    with open(file_path, 'w+') as f:
        num_chars = 100000000
        f.write('0' * num_chars)
    return file_path

def copy_file(src_path, dest_path):
    if os.path.exists(src_path):
        shutil.copy(src_path, dest_path)

def thread_handler():
    while True:
        task = q.get()
        task_type = task.get("type", None)
        task_src_path = task.get("src_path", None)
        task_dest_path = task.get("dest_path", None)
        #sys.stdout.write("task_type: %s\n" % (task_type))
        #sys.stdout.write("task_file_path: %s\n" % (task_file_path))
        if task_type == "create":
            create_file(task_src_path)
            #sys.stdout.write("creating: %s\n" % (task_src_path))
            print_q.put("creating: %s\n" % (task_src_path))

        if task_type == "copy":
            copy_file(task_src_path, task_dest_path)
            #sys.stdout.write("copying: %s to %s\n" % (task_src_path, task_dest_path))
            print_q.put("copying: %s to %s\n" % (task_src_path, task_dest_path))

        q.task_done()
        if q.empty():
            break

def print_handler():
    while True:
        print_task = print_q.get()
        sys.stdout.write("print_handler: %s\n" % (print_task))
        print_q.task_done()
        if q.empty():
            break

def report_progress_until_finished(q):
    qsize_init = q.qsize()
    print ("qsize_init %s\n" % (qsize_init))
    while not q.empty():
        portion_finished = 1 - (q.qsize() / qsize_init)
        print("Qsize: %d\n" % (q.qsize()))
        if q.empty():
            portion_finished = 1
        print("run_parallel: {:.1%} jobs are finished".format(portion_finished))


thread_list = []
print ("Starting\n")
print ("Thread_num: %d\n" % (threads_num))
maxfiles = 100

q = Queue()
print_q = Queue()

for x in range(int(threads_num/2)):
    t = threading.Thread(target = thread_handler, name = "thread_%03d" % (x))
    # this ensures the thread will die when the main thread dies
    # can set t.daemon to False if you want it to keep running
    #t.daemon = True
    print ("starting thread\n")
    t.start()
    thread_list.append(t)

t = threading.Thread(target = print_handler, name = "print_thread_%03d" % (1))
# this ensures the thread will die when the main thread dies
# can set t.daemon to False if you want it to keep running
#t.daemon = True
print ("starting thread\n")
t.start()
thread_list.append(t)

print ("active thread count: %d" % (threading.active_count()))
for i in range(0, int(maxfiles)):
    file_out_name = "%s.%04d.txt" % (filename, i)
    src_path = os.path.join(root_path, file_out_name)
    task_dict = {
        "type": "create",
        "src_path": src_path
    }
    q.put(task_dict)

#report_progress_until_finished(q)

for i in range(0, int(maxfiles)):
    file_out_name = "%s.%04d.txt" % (filename, i)
    src_path = os.path.join(root_path, file_out_name)
    dest_folder = os.path.join(root_path, "copy_folder")
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    dest_path = os.path.join(root_path, "copy_folder", file_out_name)
    task_dict = {
        "type": "copy",
        "src_path": src_path,
        "dest_path": dest_path
    }
    q.put(task_dict)

for t in thread_list:
    t.join()

# for i in range(0, int(maxfiles)):
#     file_out_name = "%s.%04d.txt" % (filename, i)
#     src_path = os.path.join(root_path, file_out_name)
#     create_file(src_path)
#     sys.stdout.write("creating: %s\n" % (src_path))
#
# for i in range(0, int(maxfiles)):
#     file_out_name = "%s.%04d.txt" % (filename, i)
#     src_path = os.path.join(root_path, file_out_name)
#     dest_folder = os.path.join(root_path, "copy_folder")
#     if not os.path.exists(dest_folder):
#         os.makedirs(dest_folder)
#     dest_path = os.path.join(root_path, "copy_folder", file_out_name)
#     if os.path.exists(src_path):
#         copy_file(src_path, dest_path)
#         sys.stdout.write("copying: %s to %s\n" % (src_path, dest_path))


print ("All Threads Complete")
