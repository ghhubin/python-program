#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os

class SearchLog:
    def __init__(self,keyfile,logpath,resultfile):
        self.keyfile = keyfile
        self.logpath = logpath
        self.resultfile = resultfile
        self.keys = [] 
        
        fh = open(keyfile,'r')
        lines = fh.readlines( )
        for line in lines:
            line = line.strip()
            if line == '':
                continue
            if line[0] == '#':
                continue
            self.keys.append(line.split()[0])
        fh.close()
        print self.keys
    
    def CheckOneFile(self,filepath,rfh):
        print filepath
        rfh.write(filepath+'\n')
        fh = open(filepath,'r')
        lines = fh.readlines()
        for line in lines: 
            for key in self.keys:
                if line.find(key) >=0:
                    print line
                    rfh.write(line+'\n')
                    break
        fh.close()

    def CheckOneFile_ADS(self,filepath,rfh):
        '''
        ADS log 
        '''
        print filepath
        rfh.write(filepath+'\n')
        fh = open(filepath,'r')
        lines = fh.readlines()
        line_num = 0
        time_str = ''
        for line in lines: 
            if line_num % 4 == 0:
                time_str = line    #每4行，是时间行
            for key in self.keys:
                if line.find(key) >=0:
                    print time_str
                    print line
                    rfh.write(time_str+'\n')
                    rfh.write(line+'\n')
                    break
            line_num += 1
        fh.close()

    def SearchFiles(self):
        if os.path.exists(self.logpath)==False:
            print(self.logpath+ ' is not exists!!')
            return -1
        elif not os.path.isdir(self.logpath):
            print(self.logpath + ' is NOT a path!')
            return -1
        files = os.listdir(self.logpath)
        fh = open(self.resultfile,'w')
        for filename in files:
            filepath = os.path.join(self.logpath, filename)
            self.CheckOneFile_ADS(filepath,fh)   #search function   CheckOneFile
        fh.close()

if __name__=='__main__':
    '''
    seach key_word in the files of the given directions
    '''
    keyfile = 'keys.txt'
    logpath = 'C:\\Users\\bill\\Desktop\\tmp\\attack\\tmp\\atkinfo'   
    resultfile = 'result.txt'    
     
    sl = SearchLog(keyfile,logpath,resultfile)
    sl.SearchFiles() 