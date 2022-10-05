import serial, time, sys

import tkinter as tk

class Tango():

    def __init__(self):

        print("constructor")
        
        try:
            self.maestro = serial.Serial('/dev/ttyACM0')
            print(self.maestro.name)
            print(self.maestro.baudrate)

        except:

            try:
                
                self.maestro = serial.Serial('/dev/ttyACM1')
                print(self.maestro.name)
                print(self.maestro.baudrate)

            except:

                print("no service ports found")
                sys.exit(0)

        #set initial values
        self.wheels = 6000
        self.turn = 6000
        self.headtilt = 6000
        self.headturn = 6000
        self.waist = 6000


        # set motors to default
        self.send(chr(0x01), self.wheels)


    def send(self, servo, target):
        print(target)
        lsb = target &0x7F
        msb = (target >> 7) & 0x7F
        cmd = chr(0xaa) + chr(0xC) + chr(0x04) + servo + chr(lsb) + chr(msb)
        self.maestro.write(cmd.encode('utf-8'))


# ---------- Method for keyboard inputs to be passed to other methods ----------

    def arrow(self, keyPressed):

        print(keyPressed.keycode)



    def runRobot(self):

        win = tk.Tk()
        win.bind('<Up>', self.moveForward)
        win.bind('<Down>', self.moveBackward)
        win.bind('<Left>', self.turnLeft)
        win.bind('<Right>', self.turnRight)
        win.bind('<w>', self.tiltHeadUp)
        win.bind('<s>', self.tiltHeadDown)
        win.bind('<a>', self.turnHeadLeft)
        win.bind('<d>', self.turnHeadRight)
        win.bind('<z>', self.twistWasteLeft)
        win.bind('<x>', self.twistWasteRight)
        win.bind('<space>', self.resetRobot)


        win.mainloop()
            #win.bind('<Left>', controller.arrow)
            #win.bind('<Down>', controller.arrow)
            #win.bind('<Right>', controller.arrow)
            #win.bind('<space>', controller.arrow)
            #win.bind('<z>', controller.arrow)
            #win.bind('<c>', controller.arrow)
            #win.bind('<w>', controller.arrow)
            #win.bind('<s>', controller.arrow)
            #win.bind('<a>', controller.arrow)
            #win.bind('<d>', controller.arrow)
            #win.bind('<9>', running = False)

            
            
        print("system exit")
        

# ---------- Methods for moving robot forwards and backwards and stopping the robot ----------
    def moveForward(self, target):
        self.wheels -= 300
        self.send(chr(0x01), self.wheels)
        print("moving forward")


    def moveBackward(self, target):
        self.wheels += 300
        self.send(chr(0x01), self.wheels)
        print("moving backwards")



    def resetRobot(self, target):
        self.wheels = 6000
        self.send(chr(0x01), self.wheels)
        print("stopping robot")




# ---------- Methods for turning robots Motor ----------


    def turnRight(self, target):
        self.turn = 6000 - 1000
        self.send(chr(0x02), self.turn)
        time.sleep(.5)
        self.send(chr(0x01), 6000)
        self.wheels = 6000
        self.send(chr(0x01), self.wheels)
        self.resetRobot()
        
        
        

        print("turning right")


    def turnLeft(self, target):
        self.turn = 6000 + 1000
        self.send(chr(0x02), self.turn)
        time.sleep(.5)

        self.send(chr(0x01), 6000)
        self.wheels = 6000
        self.send(chr(0x01), self.wheels)
        print("turning left")
        self.resetRobot()



# ---------- Methods for turning Robot's Waste ----------

    def twistWasteRight(self, target):
        print("moving waist right")
        self.waist -= 500
        self.send(chr(0x00), self.waist)

    def twistWasteLeft(self, target):
        print("moving waist left")
        self.waist += 500
        self.send(chr(0x00), self.waist)



# ---------- Methods for turning Tango's Head ----------


    def turnHeadRight(self, target):
        self.headturn -= 500
        self.send(chr(0x03), self.headturn)
        print("moving head")

    def turnHeadLeft(self, target):
        self.headturn += 500
        self.send(chr(0x03), self.headturn)
        print("moving head")


    def tiltHeadUp(self, target):

        self.headtilt += 500
        self.send(chr(0x04), self.headtilt)
        print("tilting head")

    def tiltHeadDown(self, target):

        self.headtilt -= 500
        self.send(chr(0x04), self.headtilt)
        print("tilting head")




# robot = Tango()
# robot.runRobot()















