#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os;
import sys;
import time;

#删除指定目录下N天前的文件

class DeleteLog:
    def __init__(self,filename,days):
        self.filename=filename;
        self.days=days;

    def delete(self):
        if os.path.exists(self.filename)==False:
            print(self.filename+ ' is not exists!!')
        elif os.path.isfile(self.filename):
            print(self.filename);
        elif os.path.isdir(self.filename):
            print(self.filename + ' is a path!');
            for i in [os.sep.join([self.filename,v]) for v in os.listdir(self.filename)]:
                if self.compare_file_time(i) and (os.path.isfile(i)):
                    os.remove(i);
                    print(i+' is removed!');

    def compare_file_time(self,file):
        time_of_last_mod=os.path.getmtime(file);
        days_between=(time.time()-time_of_last_mod)/(24*60*60);
        print days_between
        if days_between>self.days:
            return True;
        return False;


if __name__=='__main__':
    path='E:\\program\\testdir';
    obj=DeleteLog(path,5);
    obj.delete();
    
