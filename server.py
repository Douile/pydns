import socket
import struct
from time import sleep

ADDR = ('192.168.1.200',53)
OPCODE_DEFS = {
    0: 'QUERY',
    1: 'IQUERY',
    2: 'STATUS'
}
I_OPCODE_DEFS = {v: k for k, v in OPCODE_DEFS.items()}
TYPE_DEFS = {
    1: 'A',
    2: 'NS',
    3: 'MD',
    4: 'MF',
    5: 'CNAME',
    6: 'SOA',
    7: 'MB',
    8: 'MG',
    9: 'MR',
    10: 'NULL',
    11: 'WKS',
    12: 'PTR',
    13: 'HINFO',
    14: 'MINFO',
    15: 'MX',
    16: 'TXT',
    252: 'AXFR',
    253: 'MAILB',
    254: 'MAILA',
    255: '*'
}
I_TYPE_DEFS = {v: k for k, v in TYPE_DEFS.items()}
CLASS_DEFS = {
    1: 'IN',
    2: 'CS',
    3: 'CH',
    4: 'HS'
}
I_CLASS_DEFS = {v: k for k, v in CLASS_DEFS.items()}

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
        print('h ',h)
        headers = struct.pack('>HHHHHH',self.id,h,len(self.questions),len(self.answers),len(self.authority),len(self.addition))
        data = b''
        for r in self.questions+self.answers+self.authority+self.addition:
            data+=bytes(r)
        return headers+data
    @staticmethod
    def fromBytes(data):
        headers, questions, answers, authority, additional = unpack(data)
        return DNSPacket(headers,questions,answers,authority,additional)

class Name:
    def __init__(self,names):
        if isinstance(names,tuple) or isinstance(names,list):
            self.names = names
        elif isinstance(names,Name):
            self.names = names.names
        else:
            self.names = []
    def __repr__(self):
        name = b''
        for n in self.names:
            name += n+b'.'
        name = name[:-1]
        return name
    def __str__(self):
        return str(self.__repr__(),'utf-8')
    def __bytes__(self):
        data = b''
        for name in self.names:
            data += bytes([len(name)])+name
        data += b'\x00'
        return data

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

def bitunpack(byte,struct_s):
    a = 0
    output = []
    negator = 0
    pos = 0
    for c in struct_s:
        a += int(c)
    for b in range(0,len(struct_s)):
        length = int(struct_s[b])
        i = a-pos
        x = byte ^ negator
        y = x>>i
        output.append(y)
        negator = negator ^ (y<<i)
        pos += length
    return tuple(output)

def bitpack(struct_s,*args):
    output = 0
    t = -1
    for c in struct_s:
        t += int(c)
    pos = 0
    for b in range(0,len(struct_s)):
        length = int(struct_s[b])
        i = t-pos
        x = args[b] << i
        output = output ^ x
        pos += length
    return output

def unpack_headers(data):
    id, h, qdcount, ancount, nscount, arcount = struct.unpack('>HHHHHH',data[:12])
    qr, opcode, aa, tc, rd, ra, z, rcode = bitunpack(h,'14111134')
    return (id, qr, opcode, aa, tc, rd, ra, z, rcode, qdcount, ancount, nscount, arcount)

def unpack_question(data):
    names = []
    name_i = 0
    while 1:
        name_len = data[name_i]
        name_i += 1
        if name_len == 0:
            break
        name = data[name_i:name_i+name_len]
        names.append(name)
        name_i += name_len
    qtype, qclass = struct.unpack('>HH',data[name_i:name_i+4])
    # qtype = data[name_i:2+name_i]
    # qclass = data[2+name_i:4+name_i]
    r = 4+name_i
    return (names,qtype,qclass),r

def unpack_record(data):
    names = []
    name_i = 0
    while 1:
        name_len = data[name_i]
        name_i += 1
        if name_len == 0:
            break
        name = data[name_i:name_i+name_len]
        names.append(name)
        name_i += name_len
    type, cclass, ttl, rdlength = struct.unpack('>HHIH',data[1+name_i:11+name_i])
    # type = data[1+name_len:3+name_len]
    # cclass = data[3+name_len:4+name_len]
    # ttl = data[4+name_len:9+name_len]
    # rdlength = data[9+name_len:11+name_len]
    rdata = data[11+name_i:11+name_i+rdlength]
    r = 11+name_i+rdlength
    return (names, type, cclass, ttl, rdata), r

def unpack(data):
    # compression handling needed
    headers = unpack_headers(data)
    rdata = data[12:]
    questions = []
    for i in range(0,headers[9]): # unpack questions
        question, r = unpack_question(rdata)
        rdata = rdata[r:]
        questions.append(question)
    answers = []
    for i in range(0,headers[10]): # unpack answers
        record, r = unpack_record(rdata)
        answers.append(record)
        rdata = rdata[r:]
    authority_records = []
    for i in range(0,headers[11]): # unpack authority records
        record, r = unpack_record(rdata)
        authority_records.append(record)
        rdata = rdata[r:]
    additional_records = []
    for i in range(0,headers[12]): # unpack additional
        record, r = unpack_record(rdata)
        additional_records.append(record)
        rdata = rdata[r:]
    if len(rdata) > 0:
        print('Unused data: ',rdata)
    return headers, questions, answers, authority_records, additional_records

def dummy_response(req):
    ans = []
    for q in req.questions:
        ans.append(ARecord(q.names,3232236030))
    res = DNSPacket((req.id,1,req.opcode,req.authorative,req.truncated,req.recursive_desired,req.recursive_avail,0,req.rcode),req.questions,ans,[],[])
    return res

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.settimeout(0)
    sock.bind(ADDR)
    print('Listening on {0}'.format(ADDR[0]))
    while 1:
        try:
            data, addr = sock.recvfrom(1024)
        except (BlockingIOError,ConnectionResetError):
            try:
                sleep(0.01)
            except KeyboardInterrupt:
                print('Closing')
                break
            continue
        print('Request from {0}'.format(addr))
        req = DNSPacket.fromBytes(data)
        print(req)
        if len(req.questions) > 0:
            if req.questions[0].rname != b'home':
                res = dummy_response(req)
                print(res)
                print(data)
                print(bytes(res))
                sock.sendto(bytes(res),addr)
