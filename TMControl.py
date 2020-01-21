import threading
import queue
import socket
import serial

#ardSerial = serial.Serial('COM4',115200)

def valueMap(n,in_min,in_max,out_min,out_max):
    return round(((n-in_min)*(out_max-out_min)/(in_max-in_min)+out_min),3)

def CSCalc(cmd):
    Hexa = []
    XOR = 0

    for el in cmd:
        Hexa.append(hex(ord(el)))
    print(str(Hexa))

    for i in Hexa:
        XOR ^= int(i,16)
    print(hex(XOR))

    return str(hex(XOR))[2:].upper()
'''
TCP_IP = '169.254.108.14'#IP of Server(TM COBOT)
TCP_PORT = 5890
BUFFER_SIZE = 1024

read_q = queue.Queue()
write_q = queue.Queue()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#IPV4,TCP
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
s.connect((TCP_IP, TCP_PORT))
'''
#--------------PROCESSING----------START---------

procIP = '127.0.0.1'
procPort = 5555
procBuffer = 1024
procSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#IPV4,TCP
procSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
procSocket.bind((procIP,procPort))
procSocket.listen(1)
def procRead(socket):
    while True:
        print(f"PROCESSING Server listening to {procIP}:{procPort}")
        connection,adress = socket.accept()
        print(f"Connection from {adress} sucessful!")
        while True:
            try:
                data = connection.recv(procBuffer)
                if not data:
                    break
                msg = data.decode('utf-8')
                print(f"PROCESSING data:{msg}")
                splitRes = msg.split(",")
                #sendPTP(float(splitRes[0]),float(splitRes[1]),float(splitRes[2]),float(splitRes[3]),float(splitRes[4]),float(splitRes[5]),int(splitRes[6]),int(splitRes[7]))
            except:
                print("PROCESSING Client disconnected")
                data = None
                msg = None
                splitRes = None
                break
            
        connection.close()


procThread = threading.Thread(target=procRead,args=(procSocket,),daemon=True)
procThread.start()

#--------------PROCESSING-----------END-------
'''
def readSocket(i):
    print(f"TM Server connecting to {TCP_IP}:{TCP_PORT}")
    while True:
        global s
        data = s.recv(BUFFER_SIZE)
        if not data:
            break
        msg = data.decode('utf-8')
        print(f"TM data:{msg}")

def sendSocket(data):
    global s
    print("Sending data to TM")
    s.sendall(data.encode('UTF-8'))
    print(f"Sent {data} to TM server")


readSocketThread = threading.Thread(target=readSocket,args=(1,),daemon=True)
readSocketThread.start()


def buildCmdStr(cmd):
    CmdStr = "TMSCT,"+str(len(cmd.encode('utf-8')))+","+cmd+","
    CS = CSCalc(CmdStr)
    CmdStr = "$"+CmdStr+"*"+CS+"\r\n"
    return CmdStr

def sendPTP(X,Y,Z,RX,RY,RZ,speed,interval,):
    cmd = f'0,PTP("CPP",{X},{Y},{Z},{RX},{RY},{RZ},{speed},{interval},0,true)'
    print(cmd)
    msg = buildCmdStr(cmd)
    print(msg)
    sendSocketThread = threading.Thread(target=sendSocket,args=(msg,),daemon=True)
    sendSocketThread.start()

#sendPTP(229.000,344.437,336.089,179.785,1.570,151.766,100,200)
'''
while True:
    pass
    '''
    strRead = ardSerial.readline().decode()
    if strRead.find("block 0:") >= 0:
        xStr = strRead[strRead.find("x:"):strRead.find("y:")]
        xVal = float(xStr[3:])
        xMap = valueMap(xVal,0,319,0,500)
        #print(f"X Raw:{xVal} X Map: {xMap}")
        yStr = strRead[strRead.find("y:"):strRead.find("width:")]
        yVal = float(yStr[3:])
        yMap = valueMap(yVal,0,199,-500,500)
        #print(f"Y Raw:{yVal} Y Map: {yMap}")
        sendPTP(xMap,yMap,358.12,-178.38,0.37,91.37,20,200)
    '''
