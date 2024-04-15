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

from tictactoe import *

class Client:

    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.ttt = None
        self.start()
    
    def get_input(self):
        n = input("Enter number of rows in TicTacToe board:\n")
        while not n.isdigit() or int(n) == 0:
            n = input("Invalid number of rows.\nEnter number of rows in TicTacToe board: ")
        return n
 
    
    
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
        print(f"str_move = {str_move}, {type(str_move)}")
        str_move_list = str_move.split(",")
        int_move_list = [int(x) for x in str_move_list]
        return tuple(int_move_list)
        #return tuple([int(char) for char in str_move]) #moves are tuples



    def start(self):
        #print("start client")
        print("==================\n| TicTacToe Game |\n==================\n")
        
        
        # Fill this out
        # Try to connect to echo server
        try:
            server_sock = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
            server_sock.connect((self.server_host, self.server_port))
            
        except OSError as e:
            print ('Unable to connect to socket: ', e)
            if server_sock:
                server_sock.close()
            sys.exit(1)

        
        n_rows = self.get_input()
        #send rows to server
        self.encode_and_send_msg(server_sock, n_rows)

        #recieve rows (same var) back and decode it
        str_resp = self.recieve_and_decode_msg(server_sock)
        #print('Client received', str_resp)
        
        #create objects
        window = Window(SIZE, BLACK)
        self.ttt = TicTacToe(int(str_resp), window)
        self.ttt.display()
        
        #play game
        self.play(server_sock)
        
        # Close server socket
        server_sock.close()
        #print("end start...")



    
    def play(self, sock):
        #"play client start...")
        #create players
        user = User("User", "o")
        server = AI("Server", "x")
        
        
        while True:
            #print("start while True")
            #set current player to user
            current_player = user
            #make user move
            user_move = current_player.get_move(self.ttt)
            #print(f"client move = {user_move}")

            self.ttt.update_board(user_move, current_player)
            
            #self.ttt.move(user_move[0], user_move[1], "o")
            self.ttt.display()
            #check for game over here, if so, send back user move here and break
            if self.ttt.check_done(current_player):
                str_msg = self.convert_move_to_str(user_move)
                self.encode_and_send_msg(sock, str_msg)
                break
            
            #send user move to server
            str_msg = self.convert_move_to_str(user_move)
            self.encode_and_send_msg(sock, str_msg)
            
            #accept server move from server
            str_resp = self.recieve_and_decode_msg(sock)
            #print(f"recieved server move {str_resp}")
            server_move = self.convert_str_to_move(str_resp)
            #print(f"server move recieved: {server_move}")
            #set current player to server
            current_player = server
            #make server move
            self.ttt.update_board(server_move, current_player)
            self.ttt.display()
            #check for game over here, if so, break
            if self.ttt.check_done(current_player):
                break

        #print("client play end...")
        '''while True:
            move = ttt.user_choose() if player == "User" else ttt.server_choose()
            ttt.parse_choice(move)
            ttt.display(player)
            if ttt.check_done():
                break
            player = "Server" if player == "User" else "User"'''

def main():
    print("main client\n")
    server_host = 'localhost'
    server_port = 50007

    if len(sys.argv) > 1:
        server_host = sys.argv[1]
        server_port = int(sys.argv[2])

    client = Client(server_host, server_port)
    
    #client.start()
    #client.play(sock_read(sock))
    #what is sick, where do i put it? shouldnt it be in a loop? and the sock red, sock write, and client all take a sock argument, so which one comes first? am i supposed to even be editing in this function? or just start and play? maybe it's in start? apparently also have to write stuff in server.py. wtf

if __name__ == '__main__':
    main()