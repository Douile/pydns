import struct
from .Name import Name
from .defs import I_TYPE_DEFS, I_CLASS_DEFS

class Record:
    def __init__(self,names,type,cclass,ttl,rdata):
        self.names = Name(names)
        self.type = type
        self.cclass = cclass
        self.ttl = ttl
        self.rdata = rdata
    def __repr__(self):
        return 'Record {0} (type: {1}, class: {2}, ttl: {3}) ::: {4}'.format(self.names,self.type,self.cclass,self.ttl,self.rdata)
    def __bytes__(self):
        data = bytes(self.names)+struct.pack('>HHIH',self.type,self.cclass,self.ttl,len(self.rdata))+self.rdata
        return data
    @staticmethod
    def fromArray(array):
        o = []
        for r in array:
            if isinstance(r,tuple) or isinstance(r,list):
                o.append(Record(r[0],r[1],r[2],r[3],r[4]))
            elif isinstance(r,Record):
                o.append(r)
        return o

class ARecord(Record):
    def __init__(self,name,addr):
        rdata = struct.pack('>I',addr)
        super().__init__(name,I_TYPE_DEFS.get('A'),I_CLASS_DEFS.get('IN'),0,rdata)

class TXTRecord(Record):
    def __init__(self,name,content):
        rdata = bytes(content,'utf-8')
        rdata = struct.pack('>H',len(rdata))+rdata
        super().__init__(name,I_TYPE_DEFS.get('TXT'),I_CLASS_DEFS.get('IN'),0,rdata)

class DomainRecord(Record):
    def __init__(self,name,content):
        rdata = bytes(Name(content))
        super().__init__(name,I_TYPE_DEFS.get(self.TYPE),I_CLASS_DEFS.get('IN'),0,rdata)

class NSRecord(DomainRecord):
    TYPE = 'NS'
    
class PTRRecord(DomainRecord):
    TYPE = 'PTR'
        
def generate_record(name,binding):
    t = binding[0]
    v = binding[1]
    if t == 'A':
        return ARecord(name,v)
    elif t == 'TXT':
        return TXTRecord(name,v)
    elif t == 'NS':
        return NSRecord(name,v)
    elif t == 'PTR':
        return PTRRecord(name,v)
    return None
