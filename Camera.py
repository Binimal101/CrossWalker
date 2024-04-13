import cv2, os

class Camera:
    channels = []

    def __init__(self, channel, name="Camera"):
        self.channels.append(channel)
        self.name = name
        self.curChannel = channel

    def switchChannel(self, channel):
        if channel not in Camera.channels:
            return None

        self.camObj.release()
        self.curChannel = channel
        self.camObj = cv2.VideoCapture(self.curChannel)

    def getImageBytes(self):
        IMAGE_NAME = "/home/pi/CrossWalker/Images/placeholder"
        IMAGE_EXTENSION = ".jpg"
        ret, image = self.camObj.read()
        
        #convert frame to jpeg bytes
        if ret: #if image is valid
            cv2.imwrite(IMAGE_NAME + IMAGE_EXTENSION, image)
        else:
            return None
        
        with open(IMAGE_NAME + IMAGE_EXTENSION, 'rb') as f:
            imageBytes = f.read()
        
        os.remove(IMAGE_NAME + IMAGE_EXTENSION) #removes placeholder
        
        return imageBytes