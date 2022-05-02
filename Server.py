import socket
import threading
import time
from random import randrange
HOST = '127.0.0.1'
PORT = 65432


#client is X and server is #

def start():#This function checks if there are already 3 players playing, if there are 3 players he would not let a new player to play
    s.listen()
    while True:
        conn, addr = s.accept()
        if threading.activeCount() == 6:
            message = "We are sorry, you can not play now. 5 players already in game"
            conn.send(message.encode())
            conn.close()
        else:
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()


def strBoard (boardArr):
    str = "-----------------------------\n"
    for i in range(6):
        str+="| "
        for j in range(7):
            str+=boardArr[i][j]
            str+=" | "
        str+="\n"
        str+="-----------------------------\n"
    return str


def insertChoice(isClient, column, boardArr):
    flag = True
    i = 5
    #Trying to add a disc to the right place
    while flag and i>=0:
        if boardArr[i][column-1] == ' ':
            flag = False
            if isClient:
                boardArr[i][column-1] = 'X'
            else:
               boardArr[i][column-1] = '#'
        i = i-1
    if flag:
        return False, boardArr #the column has no place to add another disc
    return True, boardArr #A disc was added

#status return 0 if nothing happend 1 if the board is full
# 2 if server won and 3 if client won.
def checkStatus (boardArr):
    #check if server won in a row:
    counter = 0
    serverWon = False
    for i in range(6):
        counter = 0
        for j in range(7):
            if boardArr[i][j] == '#':
                counter = counter+1
            else:
                counter = 0
            if(counter==4):
                serverWon = True
    counter = 0
    if serverWon:
        return 2

    #check if client won in a row:
    clientWon = False
    for i in range(6):
        counter =0
        for j in range(7):
            if boardArr[i][j] == 'X':
                counter = counter + 1
            else:
                counter = 0
            if (counter == 4):
                clientWon = True
    counter = 0
    if clientWon:
        return 3

    #check if server won in a column:
    for j in range(7):
        counter=0
        for i in range(6):
            if boardArr[i][j] == '#':
                counter = counter +1
            else:
                counter =0
            if(counter == 4):
                serverWon = True
    counter = 0
    if serverWon:
        return 2

    #check if client won in a column:
    for j in range(7):
        counter=0
        for i in range(6):
            if boardArr[i][j] == 'X':
                counter = counter +1
                if (counter == 4):
                    return 3
            else:
                counter =0
    counter = 0

    #check if server won in a positive sloped diagonal
    for c in range(7 - 3):
        for r in range(6 - 3):
            if boardArr[r][c] == '#' and boardArr[r + 1][c + 1] == '#' and boardArr[r + 2][c + 2] == '#' and boardArr[r + 3][ c + 3] == '#':
                return 2

    #check if server won in a negatively sloped diagonal
    for c in range(7 - 3):
        for r in range(3, 6):
            if boardArr[r][c] == '#' and boardArr[r - 1][c + 1] == "#" and boardArr[r - 2][c + 2] == '#' and boardArr[r - 3][c + 3] == '#':
                return 2

    #check if client won in a positive diagonal
    for c in range(7 - 3):
        for r in range(6 - 3):
            if boardArr[r][c] == 'X' and boardArr[r + 1][c + 1] == 'X' and boardArr[r + 2][c + 2] == 'X' and boardArr[r + 3][ c + 3] == 'X':
                return 3

    #check if client won in a negatively sloped diagonal
    for c in range(7 - 3):
        for r in range(3, 6):
            if boardArr[r][c] == 'X' and boardArr[r - 1][c + 1] == "X" and boardArr[r - 2][c + 2] == 'X' and boardArr[r - 3][c + 3] == 'X':
                return 3

    #check if board is full
    fullBoard = True
    for i in range(6):
        for j in range(7):
            if boardArr[i][j] == ' ':
                fullBoard = False
    if fullBoard:
        return 1
    return 0

def printStatus (status, conn,numOfWinsServer,numOfWinsClient):
    if (status == 1):
        msg = "The game ended in a tie.\n"
        msg += "The game is over and no one won.\n"
        msg += "current scoreboard: server: "+str(numOfWinsServer)+" client: "+str(numOfWinsClient)+"\n"
        msg += "This game is ended. please press 1 to continue\n"
        conn.send(msg.encode())
        msg = conn.recv(1024)
        msg = msg.decode()
    if (status == 2):
        msg = "Server won.\n"
        msg += "The game is over.\n"
        msg += "current scoreboard: server: " + str(numOfWinsServer+1) + " client: " + str(numOfWinsClient) + "\n"
        msg += "This game is ended. please press 1 to continue\n"
        conn.send(msg.encode())
        msg = conn.recv(1024)
        msg = msg.decode()
    if (status == 3):
        msg = "Client won.\n"
        msg += "The game is over.\n"
        msg += "current scoreboard: server: " + str(numOfWinsServer) + " client: " + str(numOfWinsClient+1) + "\n"
        msg += "This game is ended. please press 1 to continue\n"
        conn.send(msg.encode())
        msg = conn.recv(1024)
        msg = msg.decode()


def resetBoard (boardArr):
    # Declaring rows
    N = 6
    # Declaring columns
    M = 7
    # using list comprehension to initializing matrix
    boardArr = [[" " for i in range(M)] for j in range(N)]
    return boardArr

def resetGame (boardArr):
    boardArr = resetBoard(boardArr)
    return boardArr


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))


def handle_client(conn, addr):
    # Declaring rows
    N = 6
    # Declaring columns
    M = 7
    # using list comprehension to initializing matrix
    boardArr = [[" " for i in range(M)] for j in range(N)]


    #start()

    counter = 0

    while True:
        counter = counter+1
        msg = "Welcome, please choose number of wins:\n"
        conn.send(msg.encode())
        msg = conn.recv(1024)
        numOfWins = int(msg.decode())
        if numOfWins > 0:
            break
        if ((counter % 5) !=0):
            round = counter // 5
            time.sleep(60*round)


    numOfWinsServer = 0
    numOfWinsClient = 0


    msg = "Please choose level 0-hard 1-easy:\n"
    conn.send(msg.encode())
    msg = conn.recv(1024)
    level = int(msg)

    while True:

        status =0
        msg = strBoard(boardArr)
        msg += "\nEnter the column you would like to add your disc: (Enter a number between 1 to 7)\n"
        conn.send(msg.encode())
        msg = conn.recv(1024)
        msg = msg.decode()
        succeed, boardArr = insertChoice(True, int(msg), boardArr)
        #Untill the client would add a good input
        while not succeed:
            msg = "You entered a column that has no place in it.\n "
            msg += "Enter a new column that you would like to add your disc: (Enter a number between 1 to 7)\n"
            conn.send(msg.encode())
            msg = conn.recv(1024)
            msg = msg.decode()
            succeed, boardArr = insertChoice(True, int(msg), boardArr)
        status = checkStatus(boardArr)
        printStatus(status,conn,numOfWinsServer,numOfWinsClient)


        if status == 0:
            succeed = False
            # Untill the servers has a good input
            if level == 1:
                while not succeed:
                    x = randrange(7)
                    succeed, boardArr = insertChoice(False, x, boardArr)
            if level == 0:
                for j in range(7):
                    if not succeed:
                        succeed, boardArr = insertChoice(False, j+1 , boardArr)
        if status == 0:
            status = checkStatus(boardArr)
            printStatus(status,conn,numOfWinsServer,numOfWinsClient)

        if(status !=0):
            boardArr = resetBoard(boardArr)




        if status == 2:
            numOfWinsServer = numOfWinsServer+1

        if status == 3:
            numOfWinsClient = numOfWinsClient+1

        if status != 0:
            if numOfWinsServer == numOfWins:
                msg = "Server won. If you want to continue type yes\n"
                conn.send(msg.encode())
                msg = conn.recv(1024)
                msg = msg.decode()
            if numOfWinsClient == numOfWins:
                msg = "Client won. If you want to continue type yes\n"
                conn.send(msg.encode())
                msg = conn.recv(1024)
                msg = msg.decode()


                if msg == 'yes':
                    boardArr = resetGame(boardArr)
                    numOfWinsServer = 0
                    numOfWinsClient = 0

                else:
                    msg += "It was nice to play. Waiting to see you again :)\n"
                    conn.send(msg.encode())
                    break
        status = 0

    conn.close()


start()




