import argparse
import sys
import socket
import struct
import threading


def print_data(text: bytes):
    '''prints the data encoded on text'''
    header = struct.calcsize("!I")
    length = struct.unpack("!I", text[:header])[0] #finds the messeage length
    data = text[header: header + length].decode("utf-8")
    print(f"Recieved data: {data}")

   
def run_server(ip, port):
    ''' Recieves an IP address and a port and creates a socket to listen and
    print the data sent to said address'''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        while True:
            s.listen(5)
            conn, addr = s.accept()
            text = conn.recv(1024)
            #thread = threading.Thread(target=print_data, args=(text,))
            #thread.start()    
            print_data(text)


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help="the server's ip")
    parser.add_argument('server_port', type=int,
                        help="the server's port")
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        run_server(args.server_ip, args.server_port)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
