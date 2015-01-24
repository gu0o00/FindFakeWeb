__author__ = 'guojian'
#coding:utf-8

from threading import Thread
import Queue, threading, sys, time, urllib

#working thread
class Worker(Thread):
    '执行任务的单个线程任务'
    worker_count = 0
    def __init__(self, workQueue, resultQueue, timeout = 0, **kwds):
        Thread.__init__(self, **kwds)
        self.id = Worker.worker_count
        Worker.worker_count += 1
        self.setDaemon(True)
        self.workQueue = workQueue
        self.resultQueue = resultQueue
        self.timeout = timeout
        self.start()
    def run(self):
        '''the get-some-work, do-some-work main loop of worker threads'''
        while True:
            try:
                #从工作队列中获取一个任务
                callable, args, kwds = self.workQueue.get(timeout=self.timeout)
                #要执行的任务
                res = callable(*args, **kwds)
                print "worker[%2d]：%s" % (self.id, str(res))
                #将任务返回的结果放在结果队列中
                self.resultQueue.put(res)
            except Queue.Empty:
                break
            except :
                print "worker[%2d]" % self.id, sys.exc_info()[:2]

class WorkerManager:
    def __init__(self, num_of_wokers = 10,timeout=1):
        self.workQueue = Queue.Queue()
        self.resultQueue = Queue.Queue()
        self.workers = []
        self.timeout = timeout
        self._createThreads(num_of_wokers)
    def _createThreads(self,num_of_workers):
        for i in range(num_of_workers):
            worker = Worker(self.workQueue, self.resultQueue, self.timeout)
            self.workers.append(worker)
    def wait_for_complete(self):
        '''...then, wait for each of them to terminate'''
        while len(self.workers):
            worker = self.workers.pop()
            worker.join()
            if worker.isAlive() and not self.workQueue.empty():
                self.workers.append(worker)
        print "All jobs are completed."
    def add_job(self, callable, *args, **kwds):
        self.workQueue.put((callable, args,kwds))
    def get_result(self, *args, **kwds):
        return self.resultQueue.get(*args, **kwds)

if __name__ == '__main__':
    def test_job(id,sleep = 0.001):
        sum = 0
        time.sleep(sleep)
        try:
            for i in range(10000):
                sum += i
        except:
            print '[%4d]' % id, sys.exc_info()[:2]
        return sum
    def test():
        print 'start testing...'
        wm = WorkerManager(10)
        for i in range(5):
            wm.add_job(test_job, i, i*0.001)
        wm.wait_for_complete()
        print 'result Queue \'s length == %d ' % wm.resultQueue.qsize()
        while wm.resultQueue.qsize():
            print wm.resultQueue.get()
        print '...end testing'

    test()