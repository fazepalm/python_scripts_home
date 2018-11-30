"""
This module provides basic threading, and logging for use in new modules
"""

import threading
import Queue
import logging
import sys
import traceback

# =============================================================================
# ThreadLogging Class
# =============================================================================


class ThreadLoggingHandling():

    def __init__( self ):
        sys.stdout.write ( 'Initializing Thread - Logging Handler \n' )

    def create_logger( self ):

        loggerFormatStr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        loggerDateStr = '%m-%d-%Y %I:%M:%S'
        formatter = logging.Formatter(fmt = loggerFormatStr, datefmt = loggerDateStr )
        logger = logging.getLogger(__name__)
        logger.setLevel( logging.DEBUG )
        ch = logging.StreamHandler()
        ch.setFormatter( formatter )
        ch.setLevel( logging.DEBUG )
        logger.addHandler( ch )

        return logger

    def start_thread( self, thread_instance, thread_queue ):
        thread_instance.start()
        thread_output = self.end_thread( thread_instance, thread_queue )
        return thread_output

    def end_thread( self, thread_instance, thread_queue ):
        thread_output_dict = {}
        thread_output_list = []
        thread_instance.join()
        thread_name = thread_instance.getName()
        while not thread_queue.empty():
            thread_output = thread_queue.get()
            thread_queue.task_done()
            thread_output_list.append( thread_output )
        thread_output_dict[thread_name] = thread_output_list

        return thread_output_dict

    def spawn_thread( self, thread_func, thread_name, *args ):
        thread_instance = threading.Thread (
                        target = thread_func,
                        name = thread_name,
                        args = args,
                        )
        return thread_instance

ThreadLoggingHandling().__main__()
