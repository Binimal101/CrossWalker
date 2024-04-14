import Camera

def analyze(imageDir):
    """
    returns data about the enviroment in the image
    PARAM imageBytes: static type defined in Camera.py
    """
    pass

def getCommand(analysisStack):
    """
    Takes information about enviroment and deduces machine commands
    PARAM enviroment: data and or flags regarding photo enviroment
    """
    recentAnalysis = analysisStack.pop()
    previousAnaysis = analysisStack.pop()