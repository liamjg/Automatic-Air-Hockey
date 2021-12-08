import serial
import time

class Comm:
    
    def __init__(self):
        print()
        print()

        # NOTE the user must ensure that the serial port and baudrate are correct
        self.__serPort = "/dev/ttyACM0"
        self.__baudRate = 9600
        self.__ser = serial.Serial(self.__serPort, self.__baudRate)
        print("Serial port " + self.__serPort + " opened  Baudrate " + str(self.__baudRate))
        
        self.__startMarker = 60
        self.__endMarker = 62

        self.__waitForArduino()

    def close_serial(self):
        self.__ser.close

    def __waitForArduino(self):

        # wait until the Arduino sends 'Arduino Ready' - allows time for Arduino reset
        # it also ensures that any bytes left over from a previous message are discarded
    
        msg = ""
        while msg.find("Arduino is ready") == -1:

            while self.__ser.inWaiting() == 0:
                pass
        
            msg = self.__recvFromArduino()

            print(msg)
            print()


    def __sendToArduino(self, sendStr):
        self.__ser.write(str(sendStr).encode('utf-8'))

    def __sendPosToArduino(self, pos):
        sendStr = '<' + str(pos) + '>'

        self.__sendToArduino(sendStr)

    def __recvFromArduino(self):
  
        ck = ""
        x = "z" # any value that is not an end- or startMarker
        byteCount = -1 # to allow for the fact that the last increment will be one too many
  
        # wait for the start character
        while  ord(x) != self.__startMarker: 
            x = self.__ser.read()
  
        # save data until the end marker is found
        while ord(x) != self.__endMarker:
            if ord(x) != self.__startMarker:
                ck = ck + str(x,'utf-8') 
                byteCount += 1
            x = self.__ser.read()
  
        return(ck)

    def run(self, position):
        #waitingForReplay = False
        
        #if waitingForReplay == False:
        self.__sendToArduino(position)
            #waitingForReply = True
        
        #if waitingForReply == True:
            
            #while self.__ser.inWaiting() == 0:
                #pass

            #dataRecvd = self.__recvFromArduino()
            #print ("Reply Received  " + dataRecvd)
    
    
            