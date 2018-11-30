####threading and logging tests
import threading
import Queue
import logging
import sys
import traceback

class ThreadTesting():

    def target_method( self, params, thread_queue):
         """
         Some operations right here
         """
         print params[0]
         return_01 = 'testing return 01'
         return_02 = 'testing return 02'

         return_list = [return_01, return_02]

         for output in return_list:
             thread_queue.put( output )

    def start_threads( self, thread_pool, thread_queue ):
        for thread_instance in thread_pool:
            thread_instance.start()
        thread_output = self.end_threads( thread_pool, thread_queue )
        return thread_output

    def end_threads( self, thread_pool, thread_queue ):
        thread_output_list = []
        for thread_instance in thread_pool:
            thread_instance.join()
            while not thread_queue.empty():
                thread_name = thread_instance.getName()

                thread_output = thread_queue.get()
                thread_queue.task_done()
                thread_output_list.append( thread_output )
                self.thread_output[thread_name] = thread_output_list

        return self.thread_output

    def spawn_thread( self, thread_func, thread_name, *args ):
        thread_instance = threading.Thread (
                        target = thread_func,
                        name = thread_name,
                        args = args,
                        )
        return thread_instance

    def __main__( self ):
        self.thread_output = {}
        thread_pool = []
        try:
            thread_queue = Queue.Queue()
            params = ['Test', 'testing']
            thread_instance_01 = self.spawn_thread( self.target_method, 'Thread1', params, thread_queue )
            thread_instance_02 = self.spawn_thread( self.target_method, 'Thread2', params, thread_queue )
            print thread_instance_01.getName()
            print thread_instance_02.getName()

            thread_pool.append( thread_instance_01 )
            thread_pool.append( thread_instance_02 )

            thread_output = self.start_threads( thread_pool, thread_queue )
            thread_queue.join()
            for thread_instance in thread_pool:
                print thread_instance.is_alive()

            print thread_output

        except Exception:
            traceback.print_exc(file=sys.stdout)

ThreadTesting().__main__()
