import struct
from .defs import TYPE_DEFS, CLASS_DEFS
from .Name import Name

class Question:
    def __init__(self,names,qtype,qclass):
        self.names = Name(names)
        self.dname = names[0]
        self.rname = names[-1]
        self.qtype = qtype
        self.qclass = qclass
    def __repr__(self):
        return 'Question {0} ({1}:{2})'.format(self.names,TYPE_DEFS.get(self.qtype),CLASS_DEFS.get(self.qclass))
    def __bytes__(self):
        data = bytes(self.names)+struct.pack('>HH',self.qtype,self.qclass)
        return data
    @staticmethod
    def fromArray(array):
        o = []
        for q in array:
            if isinstance(q,tuple) or isinstance(q,list):
                o.append(Question(q[0],q[1],q[2]))
            elif isinstance(q,Question):
                o.append(q)
        return o
