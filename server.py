#!/usr/bin/python3
# 
# Wesleyan University
# COMP 332
# Homework 2: Distributed tic-tac-toe game
#
# Jeremy Zay

import binascii
import random
import socket
import sys
import threading

from tictactoe import *

class Server():
    """
    Server for TicTacToe game
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.backlog = 1
        self.ttt = None
        self.start()
    
    
    def recieve_and_decode_msg(self, conn):
        bin_resp = conn.recv(1024)
        return bin_resp.decode('utf-8')
    
    def encode_and_send_msg(self, conn, str_msg):
        bin_msg = str_msg.encode('utf-8')
        conn.sendall(bin_msg)
 
    def convert_move_to_str(self, server_move):
        #print(f"server_move = {server_move}, {type(server_move)}")
        #return ''.join(map(str, server_move))
        return ','.join(map(str, server_move))


    def convert_str_to_move(self, str_move):
        #print(f"str_move = {str_move}, {type(str_move)}")
        str_move_list = str_move.split(",")
        int_move_list = [int(x) for x in str_move_list]
        return tuple(int_move_list)
        #return tuple([int(char) for char in str_move]) #moves are tuples


    def start(self):
        #print("start server")
        # Init server socket to listen for connections
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.bind((self.host, self.port))
            server_sock.listen(self.backlog)
        except OSError as e:
            print ("Unable to open server socket: ", e)
            if server_sock:
                server_sock.close()
                sys.exit(1)
                
        
        print("==================\n| TicTacToe Game |\n==================\n")
        # Wait for client connection
        client_conn, client_addr = server_sock.accept()
        print ('Client with address has connected', client_addr)
    
        #create ttt board of same size as clients with first message
        #accept size from user
        str_msg = self.recieve_and_decode_msg(client_conn)

        self.ttt = TicTacToe(int(str_msg), Window(SIZE, BLACK)) #never use window
        #accept n and echo back
        self.ttt.display()
        self.encode_and_send_msg(client_conn, str_msg)

        #print("starting thread line...")
        
        thread = threading.Thread(target = self.play, args = (client_conn, client_addr))
        #thread line ended
        thread.start()


    

    def play(self, conn, addr):
        #print("play server starting...")

        #print ('Serving content to client with address', addr)
        
        #create players
        user = User("User", "o")
        server = AI("Server", "x")
        
        while True:
            #print("starting while true in play...")
            
            #set current player to user
            current_player = user
            
            #accept user move from client
            str_resp = self.recieve_and_decode_msg(conn)
            #print(f"recieved user move {str_resp}")
            client_move = self.convert_str_to_move(str_resp)
            #print(f"client move = {client_move}")
            #make client move
            self.ttt.update_board(client_move, current_player)
            self.ttt.display_print()
            
            #check for game over here, if so, break (no need to send back any move)
            if self.ttt.check_done(current_player):
                break
            
            #set current player to server
            current_player = server
            
            #make server move
            server_move = current_player.get_move(self.ttt)
            self.ttt.update_board(server_move, current_player)
            #print(f"made server move {server_move}")
            self.ttt.display_print()
            
            #check for game over here, if so, send back user move here and break
            if self.ttt.check_done(current_player):
                str_msg = self.convert_move_to_str(server_move)
                self.encode_and_send_msg(conn, str_msg)
                break
              
            #send server move to client
            str_msg = self.convert_move_to_str(server_move)
            self.encode_and_send_msg(conn, str_msg)
        
        # Print data from client
        #print ('Server received', server_move)

        # Close connection to client
        conn.close()

def main():

    server_host = 'localhost'
    server_port = 50007

    if len(sys.argv) > 1:
        server_host = sys.argv[1]
        server_port = int(sys.argv[2])

    s = Server(server_host, server_port)

if __name__ == '__main__':
    main()