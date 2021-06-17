import socket
import threading
import time


# 모든 클라이언트에게 메시지를 전달하는 함수입니다.
def sendglobalmsg(msg):
    global connections
    for connection in connections:
        connection.send(msg.encode())


#클라이언트가 접속시 리스트에 해당 클라이언트를 추가하는 함수입니다.
def entermember(c, id, entermsg):
    connections.append(c)
    memberlist.append(id)
    sendglobalmsg(entermsg)

'''
현재 접속중인 클라이언트들의 리스트를 작성하는 쓰레드입니다.
반복적으로 멤버 리스트를 갱신하여 각 클라이언트로 전송합니다.
'''
def listupdate():
    global memberlist
    while True:
        try :
            temp = "mem)"
            for mem in memberlist:
                temp = temp  + "/" + mem
            sendglobalmsg(temp)
        except :
            pass
        time.sleep(3)

'''
반복적으로 클라이언트로부터 메시지를 전달받는 쓰레드입니다.
전달받는 데이터가 무슨 데이터인지 알수 없기 때문에 데이터를 전달받을때 앞에 "recv)"가 있을 경우 메시지를 전달 받은것으로,
아무것도 없을경우 클라이언트가 설정한 닉네임을 전달받은것으로 처리하게 작성하였습니다.
'''
def recvmsg(c, a):
    global connections
    while True:
        try:
            recv_msg = c.recv(1024)
            msg = recv_msg.decode()
            if not msg:
                break
            if msg[0:5] == "recv)":
                data = "msg)" + msg[5:]
                sendglobalmsg(data)
            else:
                data = "msg)" + msg + "님이 입장하였습니다."
                entermember(c, msg, data)
            print(data)
        except:
            pass
'''
또한 반대로 클라이언트에서 데이터를 전달받을때에도 어떤 데이터인지 구분을 위해 전달하는 데이터 앞에
msg), mem)을 붙여 각각 메시지, 멤버리스트로 구별할 수 있도록 작성하였습니다.
'''


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ("", 2500)
sock.bind(address)
sock.listen(1)
connections=[]
memberlist = []
print("서버를 시작합니다...")


while True:
    c, a = sock.accept()

    #멤버리스트를 갱신해주는 쓰레드
    memberThread = threading.Thread(target=listupdate)
    memberThread.daemon = True
    memberThread.start()

    #데이터를 전달받는 쓰레드
    recvandsendThread = threading.Thread(target=recvmsg, args=(c, a))
    recvandsendThread.daemon = True
    recvandsendThread.start()



