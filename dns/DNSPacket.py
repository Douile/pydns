import struct
from .utils import bitpack
from .raw import unpack
from .defs import OPCODE_DEFS
from .Question import Question
from .Record import Record

class DNSPacket:
    def __init__(self,headers,questions,answers,authority,additional):
        self.id = headers[0]
        self.qr = headers[1]
        self.opcode = headers[2]
        self.authorative = headers[3]
        self.truncated = headers[4]
        self.recursive_desired = headers[5]
        self.recursive_avail = headers[6]
        self.rcode = headers[8]
        self._headers = headers
        self.questions = Question.fromArray(questions)
        self.answers = Record.fromArray(answers)
        self.authority = Record.fromArray(authority)
        self.addition = Record.fromArray(additional)
    def __repr__(self):
        if self.qr == True:
            type = 'response'
        else:
            type = 'request'
        qs = ''
        for q in self.questions+self.answers+self.authority+self.addition:
            qs += q.__repr__()+'\n'
        return 'DNS {0} ({1}) opcode: {2}\n{4} questions {5} answers {6} authorities {7} additionals\n{3}'.format(type,self.id,OPCODE_DEFS.get(self.opcode),qs,len(self.questions),len(self.answers),len(self.authority),len(self.addition))
    def __bytes__(self):
        h = bitpack('14111134',self.qr,self.opcode,self.authorative,self.truncated,self.recursive_desired,self.recursive_avail,0,self.rcode)
        # print('h ',h)
        headers = struct.pack('>HHHHHH',self.id,h,len(self.questions),len(self.answers),len(self.authority),len(self.addition))
        data = b''
        for r in self.questions+self.answers+self.authority+self.addition:
            data+=bytes(r)
        packet = headers+data
        return packet
    @staticmethod
    def fromBytes(data):
        headers, questions, answers, authority, additional = unpack(data)
        return DNSPacket(headers,questions,answers,authority,additional)
