class Name:
    def __init__(self,names):
        if isinstance(names,tuple) or isinstance(names,list):
            self.names = names
        elif isinstance(names,Name):
            self.names = names.names
        elif isinstance(names,str):
            t_names = names.split('.')
            self.names = []
            for name in t_names:
                self.names.append(bytes(name,'utf-8'))
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
