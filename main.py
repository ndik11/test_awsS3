# person_data = ["John", "Smith", 23, "programmer"]
# user_name, user_surname, user_age, user_occupation = person_data
# print user_age

def countxz():
    f = open(r'c:/file.txt')
    text = f.readlines()
    print type(text), 'file context:  ', text
    for i in text:
        print i
        if i == 'login: fdsfsdf\n':
            print 'wow'

    # value1, value2, value3, value4 = text
    # print "VALUES:", value1, value2, value3, value4
    # list_value1 = value1.split()
    # login, login_value = list_value1
    # true_login = login[:-1]
    # print true_login,'is',  login_value
    # return 1

print countxz()



    # login, value1, passwd, value2, param, value3, time, value4 = textlist
    # print login, value1
    # for i in text:
    #     k = 0
    #     k +=1
    #     # print k
    #     print i
    # for i in text:
    #     i = (n, i[:])
    #     data.append(i)
    #     n += 1
    #     # enumerate(i)
    #     # tmp.append(i)
    # print data
    # f.close()
    # return data


# list1 = count()
# a = list1
# for i in a:
#     print "a=", a



import os

# def folder():
#     cwd = os.getcwd()
#     print cwd
#     print os.path.exists('main.py')
#     print os.listdir('../../../')
# folder()

# def walk(dir):
#   for name in os.listdir(dir):
#     path = os.path.join(dir, name)
#     if os.path.isfile(path):
#         print path
#     else:
#         walk(path)
# walk('.')

# import os, sys
# def getlocaldata(sms,dr,flst):
#    for f in flst:
#       fullf = os.path.join(dr,f)
#       if os.path.islink(fullf): continue # don't count linked files
#       if os.path.isfile(fullf):
#           sms[0] += os.path.getsize(fullf)
#           sms[1] += 1
#       else:
#           sms[2] += 1
# def dtstat(dtroot):
#    sums = [0,0,1] # 0 bytes, 0 files, 1 directory so far
#    os.path.walk(dtroot,getlocaldata,sums)
#    return sums
#
# report = dtstat('.')
# print report

# import os, sys, fnmatch
#
# mask = '*.py'
# pattern = 'import os'
#
# def walk(arg,dir,files):
#    for file in files:
#      if fnmatch.fnmatch(file,mask):
#         name = os.path.join(dir,file)
#         try:
#           data = open(name,'rb').read()
#           if data.find(pattern) != -1:
#             print name
#         except:
#             pass
# os.path.walk('../../../../',walk,[])

# import threading
# import Queue
#
# class Worker(threading.Thread):
#
#     def __init__(self, work_queue, word):
#         super(Worker,self).__init__()
#         self.work_queue = work_queue
#         self.word = word
#
#     def run(self):
#         try:
#             filename = self.work_queue.get()
#             self.process(filename)
#         finally:
#             pass
#
#     def process(self, filename):
#         previous = "
#         current=True
#         with open(filename, "rb") as fh:
#             while current:
#                 current = fh.readline()
#                 if not current: break
#                 current = current.decode("utf8", "ignore")
#                 if self.word in current :
#                     print("find {0}: {1}".format(self.word,filename))
#                 previous = current
#
# word = 'import'
# filelist = ['./file1.py','./file2.py','./file3.py']
# work_queue = Queue.Queue()
# for filename in filelist:
#     work_queue.put(filename)
# for i in range(3):
#     worker = Worker(work_queue, word)
#     worker.start()

# import time
#
# loop_count = 1000000
#
# def method1():
#   from array import array
#   char_array = array('c')
#   for num in xrange(loop_count):
#     char_array.fromstring(`num`)
#   return char_array.tostring()
#
#
# def method2():
#     str_list = []
#     for num in xrange(loop_count):
#         str_list.append(`num`)
#     return ''.join(str_list)
#
# def method3():
#   from cStringIO import StringIO
#   file_str = StringIO()
#   for num in xrange(loop_count):
#     file_str.write(`num`)
#   return file_str.getvalue()
#
# def method4():
#   return ''.join([`num` for num in xrange(loop_count)])
#
# list = method4()
# print list
# # for i in list:
# #     print i
#
# t1 = time.time()
# method1()
# t2 = time.time()
# print "\t%.1f" % ((t2 - t1))
# method2()
# t3 = time.time()
# print "\t%.1f" % ((t3 - t2))
# method3()
# t4 = time.time()
# print "\t%.1f" % ((t4 - t3))
# method4()
# t5 = time.time()
# print "\t%.1f" % ((t5 - t4))

# def f(x):
#     for y in xrange(2, x):
#         print x, '%', y
#         if x % y == 0: return 0
#     return 1
#
# print filter(f, xrange(2, 1000))

# seq1 = [1, 2, 3]
# seq2 = [4, 5, 6]
# for i, y in map(None, seq1, seq2):
#     print i, y
