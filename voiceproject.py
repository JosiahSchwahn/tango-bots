import serial, time, sys
import speech_recognition as sr
import tkinter as tk
import threading
import _thread


# class SpeechRec():

#     def __init__(self):
#         self.command = ""

#         #start thre

#     def listen(self):
#         listening = True
#         while listening:
#             with sr.Microphone() as source:
#                 r= sr.Recognizer()
#                 r.adjust_for_ambient_noise(source)
#                 r.dyanmic_energythreshhold = 3000
                
#                 try:
#                     print("listening")
#                     audio = r.listen(source)            
#                     print("Got audio")
#                     self.command = r.recognize_google(audio)
#                     #print(self.command)
#                 except sr.UnknownValueError:
#                     print("Don't knoe that werd")

#     def get_command(self):
#         return self.command




class Tango():


    def __init__(self):

        print("constructor")
        self.command = "init"
        
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
        # self.send(chr(0x00), self.waist)
        # self.send(chr(0x03), self.headtilt)
        # self.send(chr(0x04), self.headturn)

    def listen(self):
        listening = True
        while listening:
            with sr.Microphone() as source:
                r= sr.Recognizer()
                r.adjust_for_ambient_noise(source)
                r.dyanmic_energythreshhold = 3000
                
                try:
                    print("listening")
                    audio = r.listen(source)            
                    print("Got audio")
                    self.command = r.recognize_google(audio)
                    print(self.command)

                    if self.command == "go":
                        self.moveForward()

                    if self.command == "stop":
                        self.resetRobot()
                        
                    if self.command == "back":
                        self.moveBackward()
                        
                    if self.command == "left":
                        self.turnLeft()
                      
                    if self.command == "right":
                        self.turnRight()
                
                    if self.command == "look right":
                        self.turnHeadRight()
                    
                    if self.command == "look left":
                        self.turnHeadLeft()
                
                    if self.command == "body right":
                        self.twistWasteRight()
                    
                    if self.command == "body left":
                        self.twistWasteLeft()
                    
                    if self.command == "look up":
                        self.tiltHeadUp()
                    
                    if self.command == "look down":
                        self.tiltHeadDown()
                    

                except sr.UnknownValueError:
                    print("Don't know that word")

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

        # win = tk.Tk()

        # win.bind('<Up>', self.moveForward)
        # win.bind('<Down>', self.moveBackward)
        # win.bind('<Left>', self.turnLeft)
        # win.bind('<Right>', self.turnRight)
        # win.bind('<w>', self.tiltHeadUp)
        # win.bind('<s>', self.tiltHeadDown)
        # win.bind('<a>', self.turnHeadLeft)
        # win.bind('<d>', self.turnHeadRight)
        # win.bind('<z>', self.twistWasteLeft)
        # win.bind('<x>', self.twistWasteRight)
        # win.bind('<space>', self.resetRobot)

        while True:
            pass

            # if self.command == "go":
            #     self.moveForward
            #     self.command = "a"
            # if self.command == "stop":
            #     self.resetRobot
            #     self.command = "a"
            # if self.command == "back":
            #     self.moveBackward
            #     self.command = "a"
            # if self.command == "left":
            #     self.turnLeft
            #     self.command = "a"
            # if self.command == "right":
            #     self.turnRight
            #     self.command = "a"
            # if self.command == "head right":
            #     self.turnHeadRight
            #     self.command = "a"
            # if self.command == "head left":
            #     self.turnHeadLeft
            #     self.command = "a"
            # if self.command == "waist right":
            #     self.twistWasteRight
            #     self.command = "a"
            # if self.command == "waist left":
            #     self.twistWasteLeft
            #     self.command = "a"
            # if self.command == "head up":
            #     self.tiltHeadUp
            #     self.command = "a"
            # if self.command == "head down":
            #     self.tiltHeadDown
            #     self.command = "a"

            
        
            


        # win.mainloop()
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
    def moveForward(self):
        self.wheels -= 300
        self.send(chr(0x01), self.wheels)
        print("moving forward")


    def moveBackward(self):
        self.wheels += 300
        self.send(chr(0x01), self.wheels)
        print("moving backwards")



    def resetRobot(self):
        self.wheels = 6000
        self.send(chr(0x01), self.wheels)
        print("stopping robot")




# ---------- Methods for turning robots Motor ----------


    def turnRight(self):
        self.turn = 6000 - 1000
        self.send(chr(0x02), self.turn)
        time.sleep(.5)
        self.send(chr(0x01), 6000)
        self.wheels = 6000
        self.send(chr(0x01), self.wheels)
        self.resetRobot()
        
        
        

        print("turning right")


    def turnLeft(self):
        self.turn = 6000 + 1000
        self.send(chr(0x02), self.turn)
        time.sleep(.5)

        self.send(chr(0x01), 6000)
        self.wheels = 6000
        self.send(chr(0x01), self.wheels)
        print("turning left")
        self.resetRobot()



# ---------- Methods for turning Robot's Waste ----------

    def twistWasteRight(self):
        print("moving waist right")
        self.waist -= 500
        self.send(chr(0x00), self.waist)

    def twistWasteLeft(self):
        print("moving waist left")
        self.waist += 500
        self.send(chr(0x00), self.waist)



# ---------- Methods for turning Tango's Head ----------


    def turnHeadRight(self):
        self.headturn -= 500
        self.send(chr(0x03), self.headturn)
        print("moving head")

    def turnHeadLeft(self):
        self.headturn += 500
        self.send(chr(0x03), self.headturn)
        print("moving head")


    def tiltHeadUp(self):

        self.headtilt += 500
        self.send(chr(0x04), self.headtilt)
        print("tilting head")

    def tiltHeadDown(self):

        self.headtilt -= 500
        self.send(chr(0x04), self.headtilt)
        print("tilting head")


robot = Tango()
# try:
#     _thread.start_new_thread(robot.listen, ())
# except:
#     print("didnt work")
# try:
#     _thread.start_new_thread(robot.runRobot, ())
# except:
#     print("didnt work")






#robot.runRobot()
robot.listen()















