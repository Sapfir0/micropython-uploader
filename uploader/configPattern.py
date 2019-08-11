import os


def getCom(port):
    comPort = "AMPY_PORT=" + port
    return comPort


def getSpeed(preferSpeed=2):
    speed = [9600, 57600, 115200, 230400, 460800, 921600]
    boardSpeed = "AMPY_BAUD=" + str(speed[preferSpeed])
    return boardSpeed  # я так захотел


def createAmpyConfig(port, directory):
    comPort = getCom(port)
    if not os.path.exists(os.path.join(directory, ".ampy")):
        print("Config file .ampy was not found in current directory")
        with open(".ampy", "w") as f:
            f.write(comPort)
            f.write("\r\n")
            f.write(getSpeed())
        print("Config file .ampy was created")

