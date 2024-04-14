import cv2, os

class Channel:
    def __init__(self, channel):
        Camera.channels.append(channel)
        self.cameraChannelDataStack = []
    
    def getChannel(self):
        return self.curChannel
    
    def appendData(self, analysis):
        self.cameraChannelDataStack.append(analysis)

    def popData(self):
        return None if self.cameraChannelDataStack else self.cameraChannelDataStack.pop()
 
    def dataStackSize(self):
        return len(self.cameraChannelDataStack)

    def isChannelNum(self, channel):
        return self.curChannel == channel

    def fetchChannelObject(channel):
        for ch in Camera.channels:
            if ch.isChannelNum(channel):
                return ch
        return None

class Camera:
    channels = []
    def __init__(self, channel, name="Camera"):
        self.channels.append(Channel(channel))
        self.name = name
        self.curChannel = Channel.fetchChannelObject(channel)

    def switchChannel(self, channel):
        channelObj = Channel.fetchChannelObject(channel)
        if channelObj is None:
            return None

        self.camObj.release()
        self.curChannel = channelObj
        self.camObj = cv2.VideoCapture(self.curChannel.getChannel())

    def createImage(self):
        IMAGE_NAME = "/home/pi/CrossWalker/Images/placeholder{self.getChannel()}"
        IMAGE_EXTENSION = ".jpg"
        ret, image = self.camObj.read()
        
        #convert frame to jpeg bytes
        if ret: #if image is valid
            cv2.imwrite(IMAGE_NAME + IMAGE_EXTENSION, image)
        else:
            return None
        
        return IMAGE_NAME + IMAGE_EXTENSION
    
    