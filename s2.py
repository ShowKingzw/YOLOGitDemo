import select
import socket


while True:

    read_sockets, write_sockets, error_sockets = select.select(connected_clients_sockets, [], [])

    for sock in read_sockets:

        if sock == server_socket:

            sockfd, client_address = server_socket.accept()
            connected_clients_sockets.append(sockfd)

        else:
            try:

                data = sock.recv(4096)
                txt = str(data)

                if data:

                    if data.startswith('SIZE'):
                        tmp = txt.split()
                        size = int(tmp[1])

                        print 'got size'

                        sock.sendall("GOT SIZE")

                    elif data.startswith('BYE'):
                        sock.shutdown()

                    else :

                        myfile = open(basename % imgcounter, 'wb')
                        myfile.write(data)

                        data = sock.recv(40960000)
                        if not data:
                            myfile.close()
                            break
                        myfile.write(data)
                        myfile.close()

                        sock.sendall("GOT IMAGE")
                        sock.shutdown()
            except:
                sock.close()
                connected_clients_sockets.remove(sock)
                continue
        imgcounter += 1
server_socket.close()