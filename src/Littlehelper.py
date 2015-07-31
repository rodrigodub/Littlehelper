#! /usr/bin/python3

#################################################
#                   Littlehelper
# Little Helper is just an utility module for
# database and text methods
#
# v0.1.011
# Issue #5
#
# Rodrigo Nobrega
# 20150713-20150731
#################################################
__author__ = 'Rodrigo Nobrega'

# import modules
import pypyodbc
import sqlite3
import os
from ftplib import FTP
import getpass


# LHAuthenticate() was developed as Godzilla.GzAuthenticate()
# to get username and password to connect to Jira
class LHAuthenticate(object):
    def __init__(self):
        self.username = input('Username: ')
        self.pwd = getpass.getpass('Password: ')


# Class LHQuery() aggregates all functions to query the databases.
# Inherited, reused/modified from:
# Godzilla.GzQuery(),
# Difool.DfPersistence(),
# Snoopy.SnDatabaseFunctions()
class LHQuery(object):
    """
    LHQuery aggregate a number of functions to connect, query,
    and insert data into a database
    --
    TO DO: covnvert connection strings, query_db() and insert_db()
    to be used as generic
    """
    def __init__(self, user=None, pwd=None):
        self.dbCRM = r'DRIVER={SQL Server};SERVER=CROWN\PIVOTAL;DATABASE=ProductionED;Trusted_Connection=yes'
        self.dbJira = r'DRIVER=SQL Server;SERVER=JIRA;UID={};PWD={};' \
                      r'DATABASE=jiradb;Trusted_Connection=no'.format(user, pwd)
        self.dbSQLite = 'persistence.sqlite3'

    def query_db(self, mode, query, args=()):
        """
        Queries the database.
        mode: 'SQLite3' or 'SQL Server'
        query: SQL expression - strings to be replaced at ?, ?, etc
        args: strings to replace the question marks (note: finally implemented)
        """
        if mode == 'Jira':
            conn = pypyodbc.connect(self.dbJira)
        elif mode == 'CRM':
            conn = pypyodbc.connect(self.dbCRM)
        elif mode == 'SQLite3':
            conn = sqlite3.connect(self.dbSQLite)
        else:
            conn = None
        cur = conn.cursor()
        cur.execute(query, args)
        rv = cur.fetchall()
        cur.close()
        conn.commit()
        return rv

    def insert_db(self, mode, query, args=()):
        """
        Inserts into the database.
        mode: 'SQLite3' or 'SQL Server'
        query: SQL expression - strings to be replaced at ?, ?, etc
        args: strings to replace the question marks
        """
        if mode == 'Jira':
            conn = pypyodbc.connect(self.dbJira)
        elif mode == 'CRM':
            conn = pypyodbc.connect(self.dbCRM)
        elif mode == 'SQLite3':
            conn = sqlite3.connect(self.dbSQLite)
        else:
            conn = None
        c = conn.cursor()
        c.execute(query, args)
        conn.commit()
        return True


# LHFile
# reused from Difool.DfLogFile()
class LHFile(object):
    """
    DfLogFile opens a file, appends new info at the end, and closes it.
        Modified on v0.1.0810 to receive the filename when instantiated
    """
    def __init__(self, file):
        """
        :param file: string     - the log file, usually declared as variable LOGFILE
        """
        self.file = r'{}'.format(file)

    def writeInfo(self, param):
        """
        Method to open a file in Append mode, write the argument passed as param,
        add a new line, and close the file for writing.
        :param param: string    - what to write to the log file
        """
        # open file in Append mode
        f = open(self.file, 'a')
        # write to file the argument param, and a new line
        f.write(param)
        f.write('\n')
        # close the file
        f.close()

    def readInfo(self):
        """
        Method to scan the file, returns a list
        """
        arq = open(self.file, 'r')
        # arq = open(self.file, encoding='latin-1')
        result = []
        #arq.readline()
        [result.append(i) for i in arq]
        arq.close()
        return result


class LHFtp(object):
    """
    LHFtp is a class to provide FTP upload and download methods
    ------
    Usage:
    ------
    x = LHFtp('ftpserver.com.au', user=LHAuthenticate)
        connects to 'ftpserver.com.au', using an LHAuthenticate instance as the user

    x.setRemoteDir('newDirectory')
        changes FTP working directory to 'newDirectory'

    x.setLocalDir('newLocalDirectory')
        changes Local computer directory to 'newLocalDirectory'

    x.uploadFile('filename')
        uploads 'filename' to FTP working directory

    x.downloadFile('filename')
        downloads 'filename' to Local working directory

    x.quit()
        closes FTP connection
    """
    def __init__(self, ftpserver, authentication=LHAuthenticate):
        # connect and login
        self.ftp = FTP(ftpserver)
        self.ftp.login(user=authentication.username, passwd=authentication.pwd)
        # acknowledge and list
        print('Connected to {}'.format(ftpserver))
        self.ftp.dir()

    def setRemoteDir(self, wd):
        """Change FTP server working directory"""
        try:
            self.ftp.cwd(wd)
            print('Remote directory changed to {}'.format(wd))
            # self.ftp.dir()
        except:
            print('Remote directory does not exist.')

    def setLocalDir(self, wd):
        """Change Local computer working directory"""
        try:
            os.chdir(wd)
            print('Local directory changed to {}'.format(os.getcwd()))
        except:
            print('Local directory does not exist.')

    def uploadFile(self, filename):
        """Upload file to the current FTP working directory"""
        print('Uploading...')
        self.ftp.storbinary('STOR ' + filename, open(filename, 'rb'))
        print('{} uploaded to {}'.format(filename, self.ftp.pwd()))
        return

    def downloadFile(self, filename):
        """Download file to the local directory"""
        print('Downloading...')
        localfile = open(filename, 'wb')
        self.ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
        localfile.close()
        print('{} downloaded to {}'.format(filename, os.getcwd()))
        return

    def quit(self):
        """Quit FTP connection"""
        self.ftp.quit()
        print('Goodbye.')


# test loop
def test():
    print('------------------------')
    print('Test.')
    print('------------------------')


# main loop
def main():
    print('------------------------')
    print('Main.')
    print('------------------------')


# main, calling main loop
if __name__ == '__main__':
    # test()
    main()
