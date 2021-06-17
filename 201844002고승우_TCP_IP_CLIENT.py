import tkinter as tk
import socket
import threading
import tkinter.messagebox

def main():
    #데이터를 서버로 전달하는 함수입니다.
    def sendmsg():
        msg = 'recv)' + id + " : " + str(send_msg.get())
        send_msg.delete("0", "end")
        print(msg)
        sock.send(msg.encode())

    #반복적으로 클라이언트로부터 데이터를 전송받는 쓰레드입니다.
    #데이터 앞의 mem)은 멤버 리스트를, msg)는 메시지를 전달받았음을 의미합니다.
    def recv_msg(sock):
        while True:
            try:
                recv_msg = sock.recv(1024)
                msg = recv_msg.decode()
                print(msg)
                if not recv_msg:
                    break
                if msg[0:4] == "mem)":
                    updatemember(msg)
                elif msg[0:4] == "msg)":
                    data = msg[4:]+'\n'
                    print(data)
                    textbox.insert("current", data)
                else :
                    pass
            except:
                pass

    #접속자 목록을 갱신해주는 함수입니다.
    def updatemember(msg):
        try:
            memlist = msg.split('/')
            del memlist[0]
            cnt.set("접속자 목록 : " + memlist)
            setname.update()
        except:
            pass

    def start():
        global sock
        global id
        svrIP = str(svr.get())
        id = str(input_id.get())

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            BUFSIZE = 1024
            port = 2500

            sock.connect((svrIP, port))
        except:
            tk.messagebox.showerror('연결 오류', '접속에 실패했습니다.')
            exit(4)

        #데이터를 전달받는 쓰레드
        recvmsgthread = threading.Thread(target=recv_msg, args=(sock,))
        recvmsgthread.daemon = True
        recvmsgthread.start()


        #닉네임을 입력하지 않았을시 진행되지 않도록 처리했습니다.
        if not id :
            tk.messagebox.showerror("닉네임 오류", "닉네임을 입력해주세요")
        else :
            sock.send(id.encode())

            insert_ip.destroy()
            svr.destroy()
            id_insert.destroy()
            input_id.destroy()
            input_id_btn.destroy()

            ip = tk.Label(setname, text=svrIP + "의 채팅방")

            textbox.pack(fill='x')
            cnt.pack()
            ip.pack()
            send_msg.pack()
            send_btn.pack()
            send_msg.focus()

    setname = tk.Tk()
    setname.title("채팅창")
    setname.geometry("200x400")

    insert_ip = tk.Label(setname, text="서버 아이피 입력")
    cnt = tk.Label(setname, text="")
    textbox = tk.Text(setname, height=20)

    svr = tk.Entry(setname)
    svr.insert("0", "127.0.0.1")
    id_insert = tk.Label(setname, text="닉네임 입력")
    input_id = tk.Entry(setname)
    input_id_btn = tk.Button(setname, text='입장', command=start)

    send_msg = tk.Entry(setname)
    send_btn = tk.Button(setname, text='전송', command=sendmsg)

    cnt.pack()
    insert_ip.pack()
    svr.pack()
    id_insert.pack()
    input_id.pack()
    input_id_btn.pack()
    input_id.pack()
    input_id.focus()
    setname.mainloop()



if __name__ == "__main__":
    main()
