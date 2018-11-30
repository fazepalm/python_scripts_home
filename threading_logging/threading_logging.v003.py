import traceback
import sys
import Queue

import utilThreadLogging as UTL

class ThreadTesting():

    def target_method_01( self, params, thread_queue):
         """
         Some operations right here
         """
         return_01 = params[0]

         return_list = [return_01]

         for output in return_list:
             thread_queue.put( output )

    def target_method_02( self, params, thread_queue):
         """
         Some operations right here
         """
         return_02 = 'Test target_method_02!'

         return_list = [return_02]

         for output in return_list:
             thread_queue.put( output )

    def __main__( self ):
        UTL_spawn_thread = UTL.ThreadHandler().spawn_thread
        UTL_start_thread = UTL.ThreadHandler().start_thread
        UTL_create_logger = UTL.LoggingHandler().create_logger()
        thread_pool = []
        thread_output_list = []
        logger = UTL_create_logger
        try:
            thread_queue = Queue.Queue()
            target_list = [ self.target_method_01, self.target_method_02 ]

            for thread_count, target in enumerate( target_list ):
                thread_name = 'Thread_%02d' % ( thread_count )
                thread_param = [ 'Return_%02d' % ( thread_count ) ]
                thread_instance = UTL_spawn_thread( target, thread_name, thread_param, thread_queue )
                thread_pool.append( thread_instance )

            for thread_instance in thread_pool:
                #print thread_instance.getName()
                thread_output = UTL_start_thread( thread_instance, thread_queue )
                thread_queue.join()
                #print thread_instance.is_alive()
                thread_output_list.append( thread_output )

            for output in thread_output_list:
                logger.debug( output )
                # for t_count, ( o_thread_name, o_thread_output ) in enumerate( output.iteritems() ):
                #     logger.debug( o_thread_name )
                #     logger.debug( o_thread_output )

        except Exception:
            traceback.print_exc( file=sys.stdout )

ThreadTesting().__main__()
