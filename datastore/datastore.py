import redis, pymongo, pickle
from bson import Binary
import numpy as np

def np2bson(data):
    return Binary( pickle.dumps( data, protocol=2) ) 

def bson2np(data):
    return pickle.loads(data)

class dbStore(object):
    """
    just a prototype
    """
    def __init__(self, ip = "localhost", port = "80"):
        self.ip = ip
        self.port = port
    
    def get(self, name):
        pass
    
    def set(self, name, value):
        pass
    
class rstore(dbStore):
    
    def __init__(self, ip = "localhost", port = "6379"):
        super(rstore, self).__init__(ip = ip, port = port)
        self.db = redis.StrictRedis(host=ip, port=int(port), db=0)
        self.nd = {}
        
    def get(self, name):
        record = self.db.get(name)
        if name in self.nd.keys():
            record = bson2np(record)
        return record

    def set(self, name, value):
        if isinstance(value, np.ndarray):
            self.nd[name] = value.shape
            value = np2bson(value)
        self.db.set(name,value)
        
class mstore(dbStore):
    
    def __init__(self, ip = "localhost", port = "6379", session = "default"):
        super(mstore, self).__init__(ip = ip, port = port)
        mongo = pymongo.Connection(ip)
        mongo_db = mongo['py_datastore']
        self.db = mongo_db[session]
        
        self.nd = {}
        
    def get(self, name):
        record = self.db.find_one({"name":name})['value']
        if isinstance(record,Binary):
            record = bson2np(record)
        return record

    def set(self, name, value):
        if isinstance(value, np.ndarray):
            self.nd[name] = value.shape
            value = np2bson(value)
        self.db.update({"name":name},{"$set":{"value":value}},  upsert=True)        
        
if __name__ == "__main__":
    import numpy as np
    import time
    x = mstore()
    
    t = time.time()
    x.set("pi",np.random.randn(14,1000))
    
    val = x.get("pi")
    print val
    print time.time() - t
