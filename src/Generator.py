#!/usr/bin/env python
# $Id$

from Error import GeneratorError

from syslog import syslog, LOG_ERR

class Generator(object):
    '''This is a class that generators can be subclassed from.
    __name__, __version__, and __author__ must be set for the module
    __build__ is a dictionary mapping filename to generator function
    __requires__ is a set of external published data needed for operation'''
    
    __name__ = None
    __version__ = None
    __datastore__ = '/home/desai/data/b2'
    __build__ = {}
    __requires__ = []
    
    def __init__(self, core):
        self.core=core
        self.data="%s/%s"%(self.__datastore__,self.__name__)
        self.__setup__()

    def __setup__(self):
        '''This method must be overloaded during subclassing.
        All module specific setup, including all publication, occurs here.'''

    def CompleteSetup(self):
        self.ReadAll()
        print "%s loaded"%(self.__version__)

    def Cron(self):
        '''Cron defines periodic tasks to maintain data coherence'''
        pass

    def Build(self,filename,client):
        '''Build will construct a Config File object for client.'''
        if self.__build__.has_key(filename):
            return getattr(self,self.__build__[filename])(filename,client)
        else:
            raise GeneratorError, ("Key",filename)

    def Publish(self,key,value):
        self.core.Publish(self.__name__,key,value)

    def Read(self,key):
        self.core.ReadValue(key)

    def ReadAll(self):
        self.external = {}
        for field in self.__requires__:
            self.external[field] = self.Read(field)

    def GetMetadata(self,client,field):
        '''GetMetadata returns current metadata file client. Field can be one of:
        image, tags, bundles'''
        pass

    def Notify(self,region):
        '''Generate change notification for region'''
        pass

