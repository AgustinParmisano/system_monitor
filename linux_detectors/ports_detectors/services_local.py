import psutil
import socket
import time
from datetime import datetime

rows = []
lc = psutil.net_connections('inet')
logfilepath = "services.log"

while True:
    time.sleep(5)
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
            print(str(port))
            service["port"] = str(port)
            service["proto"] = str(proto_s)
            services.append(service)

    datetime_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    data = {"date": datetime_now, "services":services}
    #print(data)
    logfile_virtual = open(logfilepath,"a+")
    logfile_virtual.write(str(data) + "\r\n ")