import psutil
import socket
import time
from pprint import pprint
from datetime import datetime
from pymongo import MongoClient

#DB Connection
client = MongoClient(port=27017)
db=client.services

rows = []
logfilepath = "services.log"

def check_db_services(data):
    if (db.services.count() == 0):
        print("Fist data, add")
        result=db.services.insert_one(data)
        return True

    cursor = db.services.find({}).sort([("date",-1)]).limit(1)

    for services_db in cursor: 
        last_db_services = services_db["services"]

    if (last_db_services == data["services"]):
        pass
        print("No changes in services found. Update, not add")
        query = {"_id":services_db["_id"]}
        new_value = { "$set": {"date":data["date"]} }
        db.services.update_one(query,new_value)
    else:
        print("New changes in services found, add")
        result=db.services.insert_one(data)
    
    return True

while True:
    time.sleep(2)
    lc = psutil.net_connections('inet')
    services = []
    for c in lc:
        (ip, port) = c.laddr
        if ip == '0.0.0.0' or ip == '::':
            if c.type == socket.SOCK_STREAM and c.status == psutil.CONN_LISTEN:
                proto_s = 'tcp'
            elif c.type == socket.SOCK_DGRAM:
                proto_s = 'udp'
            else:
                continue
            pid_s = str(c.pid) if c.pid else '(unknown)'
            msg = 'PID {} is listening on port {}/{} for all IPs.'
            msg = msg.format(pid_s, port, proto_s)
            service = {}
            service["port"] = str(port)
            service["proto"] = str(proto_s)
            service = str(port) + "/" + str(proto_s)
            services.append(service)

    datetime_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    data = {"date": datetime_now, "services":services}
    #print(data)
    #logfile_virtual = open(logfilepath,"a+")
    #logfile_virtual.write(str(data) + "\r\n ")
    check_db_services(data)

    for i in db.services.find():
        pprint(i)
