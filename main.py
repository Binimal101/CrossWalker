from Camera import Camera
from ImageRecognition import analyze, getCommand
import cv2, os, serial

#Global Access Variables
commandNumber = 0 #used to organize buffer streams
SERPATH = '/dev/tty.usbserial' #TODO check serial path

def main():
    Camera(2, "Orange Camera With Sticky @channel = 2") #Bottom Left USB
    Camera(4, "Orange Camera Without Sticky @channel = 4")
    Camera(6, "Black Camera @channel = 6") #Top Left USB
 
    ch = 0 #initial
    
    ser = serial.Serial(SERPATH, 9600, timeout=0.5)
    
    while True:
        Camera.switchChannel(Camera.channels[ch])
        ch = (( (ch / 2) % 3) * 2) + 2 # oscillates between 2, 4, 6

        enviroment = analyze(Camera.getImageBytes())
        command = getCommand(enviroment)
        commandNumber += 1

        """
        Transmit command to either of the following formats:
        
        move forward ::= FORWARD
        discontinue movement or remain still ::= STOP
        turn by float angle off vertical axis (birds eye) ::= TURN (degrees: float)
        move backwards ::= BACKWARD
        next command ::= \n
        """

        #sends command info and priority num to Arduino
        ser.write((commandNumber+command+'\n').encode('utf-8'))

    ser.close()

if __name__ == "__main__":
    main()