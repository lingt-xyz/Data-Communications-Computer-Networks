DEFAULT_WAIT_TIME = 10


class Window:
    windowSize = None
    windowStart = 0

    frameHandled = None
    frameData = None
    frameTimer = None

    sendPacket = None
    getResponse = None

    def __init__(self, windowSize, sendPacket, getResponse):
        self.windowSize = windowSize
        self.sendPacket = sendPacket
        self.getResponse = getResponse

        self.frameHandled = [False] * self.windowSize
        self.frameData = [None] * self.windowSize
        self.frameTimer = [0] * self.windowSize

    def finished(self):
        for i in range(0, self.windowSize):
            if not self.frameHandled[i]:
                return False

        return True

    def getMessage(self):
        output = ""

        for i in range(0, self.windowSize):
            output = output + self.frameData[i]

        return output.rstrip()