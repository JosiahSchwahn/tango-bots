from cProfile import label
from email.mime import image
import tkinter as tk
from tkinter import ttk
#import pyttsx3
from PIL import ImageTk, Image
#import speech_recognition as sr

#import serial, time, sys

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



# ---------- Methods for moving robot forwards and backwards and stopping the robot ----------
    def speak(self, input0 = ""):
        if input0 == "":
            print("Enter input:")
            input1 = input()
            engine = pyttsx3.init()
            engine.say(input1)
            engine.runAndWait()
        else:
            engine = pyttsx3.init()
            engine.say(input0)
            engine.runAndWait()

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
                    word = r.recognize_google(audio)
                    self.speak(word)
                    listening = False
                except sr.UnknownValueError:
                    print("Don't knoe that werd")

    def moveForward(self, target):
        self.wheels = target
        self.send(chr(0x01), self.wheels)
        print("moving forward")


    def moveBackward(self, target):
        self.wheels = target
        self.send(chr(0x01), self.wheels)
        print("moving backwards")



    def resetRobot(self):
        self.wheels = 6000
        self.send(chr(0x01), self.wheels)
        print("stopping robot")




# ---------- Methods for turning robots Motor ----------


    def turnRight(self, target):
        self.turn = 6000 - 2000
        self.send(chr(0x02), self.turn)
        time.sleep(.5)
        self.send(chr(0x01), 6000)
        self.wheels = 6000
        self.send(chr(0x01), self.wheels)
        self.resetRobot()
        
        
        

        print("turning right")


    def turnLeft(self, target):
        self.turn = 6000 + 2000
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
        self.waist = target
        self.send(chr(0x00), self.waist)

    def twistWasteLeft(self, target):
        print("moving waist left")
        self.waist = target
        self.send(chr(0x00), self.waist)



# ---------- Methods for turning Tango's Head ----------


    def turnHeadRight(self, target):
        self.headturn = target
        self.send(chr(0x03), self.headturn)
        print("moving head")

    def turnHeadLeft(self, target):
        self.headturn = target
        self.send(chr(0x03), self.headturn)
        print("moving head")


    def tiltHeadUp(self, target):

        self.headtilt = target
        self.send(chr(0x04), self.headtilt)
        print("tilting head")

    def tiltHeadDown(self, target):

        self.headtilt = target
        self.send(chr(0x04), self.headtilt)
        print("tilting head")

class Gui():
    def __init__(self) -> None:
        self.selected = None

        # This list of dicts is defines the control sequence
        self.sequence = [{"command":"" , "value":6000, "time":0},
                            {"command":"" , "value":6000, "time":0},
                            {"command":"" , "value":6000, "time":0},
                            {"command":"" , "value":6000, "time":0},
                            {"command":"" , "value":6000, "time":0},
                            {"command":"" , "value":6000, "time":0},
                            {"command":"" , "value":6000, "time":0},
                            {"command":"" , "value":6000, "time":0}]

        root = self.createwindowandbuttons()
        self.root = root
        root.mainloop()

    def createwindowandbuttons(self):

        # Create window
        root = tk.Tk()
        root.geometry('1200x800')
        root.title('Robo Sequencer')



        # create buttons #####################################################################################

        #create sliders and such

        # move button
        drive_icon = ImageTk.PhotoImage(Image.open("./assets/drive.png"))
        drive_button = ttk.Button(root, image=drive_icon, command=lambda: self.select("drive"))
        drive_button.image = drive_icon
        drive_button.place( x=0, y=5)

        # turn button
        turn_icon = ImageTk.PhotoImage(Image.open("./assets/turn.png"))
        turn_button = ttk.Button(root, image=turn_icon, command=lambda: self.select("turn"))
        turn_button.image = turn_icon
        turn_button.place( x=0, y=70)

        #head tilt button
        head_tilt_icon = ImageTk.PhotoImage(Image.open("./assets/headtilt.png"))
        head_tilt_button = ttk.Button(root, image=head_tilt_icon, command=lambda: self.select("headtilt"))
        head_tilt_icon.image = head_tilt_icon
        head_tilt_button.place(x= 0, y= 140)

        #head turn button
        head_turn_icon = ImageTk.PhotoImage(Image.open("./assets/headturn.png"))
        head_turn_button = ttk.Button(root, image=head_turn_icon, command=lambda: self.select("headturn"))
        head_turn_icon.image = head_turn_icon
        head_turn_button.place(x=0, y= 210)

        #body turn
        body_turn_icon = ImageTk.PhotoImage(Image.open("./assets/bodyturn.png"))
        body_turn_button = ttk.Button(root, image=body_turn_icon, command=lambda: self.select("bodyturn"))
        body_turn_icon.image = body_turn_icon
        body_turn_button.place(x=0, y=280)



        # run button


        run_icon = ImageTk.PhotoImage(Image.open("./assets/runButton.png"))
        run_button = ttk.Button(root, image=run_icon, command=lambda: self.run())
        run_button.image = run_icon
        run_button.place(x=700, y=5)



        #pause button

        pause_icon = ImageTk.PhotoImage(Image.open("./Josiah GUI/PAUSE00.png"))
        pause_button = ttk.Button(root, image=pause_icon, command=lambda: self.select("pause"))
        pause_icon.image = pause_icon
        pause_button.place(x=700, y = 100)

        # keyboard button

        key_icon = ImageTk.PhotoImage(Image.open("./assets/keyboard.png"))
        key_button = ttk.Button(root, image=key_icon, command=lambda: self.select("keyboard"))
        key_icon.image = key_icon
        key_button.place(x=700, y=200)


        #speech button

        speech_icon = ImageTk.PhotoImage(Image.open("./assets/speech.png"))
        speech_button = ttk.Button(root, image=speech_icon, command=lambda: self.select("speech"))
        speech_icon.image = speech_icon
        speech_button.place(x=700, y = 300)



        #running animation

        animation_file = './Josiah GUI/RUN_ANIMATION_1.gif'
        info = Image.open(animation_file)
        frames = info.n_frames
        print(frames)

        #im = [tk.PhotoImage(file= animation_file, format=f'gif -index{i}') for i in range(frames)]





        #Sequence Slots and Sliders
        xadd = 10
        empty_icon = ImageTk.PhotoImage(Image.open("./assets/bluesquare.JPG"))
        # 1
        seq_button1 = ttk.Button(root, image=empty_icon, command=lambda: self.sequenceslot(seq_button1, 0))
        seq_button1.image = empty_icon
        seq_button1.place( x=75+xadd, y=5)

        slider_v1 = tk.Scale(root, from_=4000, to=8000, length=120, orient='vertical', command=self.update_slider_v1)
        slider_v1.place(x=75+xadd, y=105)
        slider_v1.set(6000)

        slider_t1 = tk.Scale(root, from_=0, to=30, length=120, orient='vertical', command=self.update_slider_t1)
        slider_t1.place(x=90+xadd, y=250)
        # 2
        seq_button2 = ttk.Button(root, image=empty_icon, command=lambda: self.sequenceslot(seq_button2, 1))
        seq_button2.image = empty_icon
        seq_button2.place( x=150+xadd, y=5)

        slider_v2 = tk.Scale(root, from_=4000, to=8000, length=120, orient='vertical', command=self.update_slider_v2)
        slider_v2.place(x=150+xadd, y=105)
        slider_v2.set(6000)

        slider_t2 = tk.Scale(root, from_=0, to=30, length=120, orient='vertical', command=self.update_slider_t2)
        slider_t2.place(x=165+xadd, y=250)
        # 3
        seq_button3 = ttk.Button(root, image=empty_icon, command=lambda: self.sequenceslot(seq_button3, 2))
        seq_button3.image = empty_icon
        seq_button3.place( x=225+xadd, y=5)

        slider_v3 = tk.Scale(root, from_=4000, to=8000, length=120, orient='vertical', command=self.update_slider_v3)
        slider_v3.place(x=225+xadd, y=105)
        slider_v3.set(6000)

        slider_t3 = tk.Scale(root, from_=0, to=30, length=120, orient='vertical', command=self.update_slider_t3)
        slider_t3.place(x=240+xadd, y=250)

        # 4
        seq_button4 = ttk.Button(root, image=empty_icon, command=lambda: self.sequenceslot(seq_button4, 3))
        seq_button4.image = empty_icon
        seq_button4.place( x=300+xadd, y=5)

        slider_v4 = tk.Scale(root, from_=4000, to=8000, length=120, orient='vertical', command=self.update_slider_v4)
        slider_v4.place(x=300+xadd, y=105)
        slider_v4.set(6000)

        slider_t4 = tk.Scale(root, from_=0, to=30, length=120, orient='vertical', command=self.update_slider_t4)
        slider_t4.place(x=315+xadd, y=250)

        # 5
        seq_button5 = ttk.Button(root, image=empty_icon, command=lambda: self.sequenceslot(seq_button5, 4))
        seq_button5.image = empty_icon
        seq_button5.place( x=375+xadd, y=5)

        slider_v5 = tk.Scale(root, from_=4000, to=8000, length=120, orient='vertical', command=self.update_slider_v5)
        slider_v5.place(x=375+xadd, y=105)
        slider_v5.set(6000)

        slider_t5 = tk.Scale(root, from_=0, to=30, length=120, orient='vertical', command=self.update_slider_t5)
        slider_t5.place(x=400+xadd, y=250)

        # 6
        seq_button6 = ttk.Button(root, image=empty_icon, command=lambda: self.sequenceslot(seq_button6, 5))
        seq_button6.image = empty_icon
        seq_button6.place( x=450+xadd, y=5)

        slider_v6 = tk.Scale(root, from_=4000, to=8000, length=120, orient='vertical', command=self.update_slider_v6)
        slider_v6.place(x=450+xadd, y=105)
        slider_v6.set(6000)

        slider_t6 = tk.Scale(root, from_=0, to=30, length=120, orient='vertical', command=self.update_slider_t6)
        slider_t6.place(x=465+xadd, y=250)

        # 7
        seq_button7 = ttk.Button(root, image=empty_icon, command=lambda: self.sequenceslot(seq_button7, 6))
        seq_button7.image = empty_icon
        seq_button7.place( x=525+xadd, y=5)

        slider_v7 = tk.Scale(root, from_=4000, to=8000, length=120, orient='vertical', command=self.update_slider_v7)
        slider_v7.place(x=525+xadd, y=105)
        slider_v7.set(6000)

        slider_t7 = tk.Scale(root, from_=0, to=30, length=120, orient='vertical', command=self.update_slider_t7)
        slider_t7.place(x=540+xadd, y=250)

        # 8
        seq_button8 = ttk.Button(root, image=empty_icon, command=lambda: self.sequenceslot(seq_button8, 7))
        seq_button8.image = empty_icon
        seq_button8.place( x=600+xadd, y=5)

        slider_v8 = tk.Scale(root, from_=4000, to=8000, length=120, orient='vertical', command=self.update_slider_v8)
        slider_v8.place(x=600+xadd, y=105)
        slider_v8.set(6000)

        slider_t8 = tk.Scale(root, from_=0, to=30, length=120, orient='vertical', command=self.update_slider_t8)
        slider_t8.place(x=615+xadd, y=250)

        # /create buttons ####################################################################################

        return root

    def update_slider_v1(self, event): self.sequence[0]["value"] = event
    def update_slider_v2(self, event): self.sequence[1]["value"] = event
    def update_slider_v3(self, event): self.sequence[2]["value"] = event
    def update_slider_v4(self, event): self.sequence[3]["value"] = event
    def update_slider_v5(self, event): self.sequence[4]["value"] = event
    def update_slider_v6(self, event): self.sequence[5]["value"] = event
    def update_slider_v7(self, event): self.sequence[6]["value"] = event
    def update_slider_v8(self, event): self.sequence[7]["value"] = event

    def update_slider_t1(self, event): self.sequence[0]["time"] = event
    def update_slider_t2(self, event): self.sequence[1]["time"] = event
    def update_slider_t3(self, event): self.sequence[2]["time"] = event
    def update_slider_t4(self, event): self.sequence[3]["time"] = event
    def update_slider_t5(self, event): self.sequence[4]["time"] = event
    def update_slider_t6(self, event): self.sequence[5]["time"] = event
    def update_slider_t7(self, event): self.sequence[6]["time"] = event
    def update_slider_t8(self, event): self.sequence[7]["time"] = event

    def sequenceslot(self, button, slot):
        #clear button and values if none is selected
        if self.selected == None:
            print("Nothing selected, clearing slot")
            new_icon = ImageTk.PhotoImage(Image.open("./assets/bluesquare.JPG"))
            button.config(image=new_icon)
            button.image = new_icon

            self.sequence[slot] = {"command":"" , "value":6000, "time":0}
            return

        print("Sequence slot ", slot, " changed to " + self.selected)

        #change image to new command
        image_address = "./assets/" + self.selected + ".png"
        new_icon = ImageTk.PhotoImage(Image.open(image_address))
        button.config(image=new_icon)
        button.image = new_icon

        #update sequence
        self.sequence[slot]["command"] = self.selected

        self.selected = None


    def select(self, selection):
        self.selected = selection



    def run(self, gif_label=None):
        robot = Tango()

        root = tk.Tk()

        run_animation = True

        while run_animation:
            file = "./assets/RUN.gif"
            info = Image.open(file)

            frames = info.n_frames  # gives total number of frames that gif contains

            # creating list of PhotoImage objects for each frames
            im = [tk.PhotoImage(file=file, format=f"gif -index {i}") for i in range(frames)]
            im.place(x=0, y=0)

            count = 0
            anim = None

            def animation(count):
                global anim
                im2 = im[count]

                gif_label.configure(image=im2)
                count += 1
                if count == frames:
                    count = 0
                anim = root.after(50, lambda: animation(count))

            gif_label = tk.Label(root, image="")
            gif_label.pack()

            animation(count)

        print("reset complete")
        for s in self.sequence:
            print(s)
            if s['command'] == "drive":
                robot.moveForward(6000)
                time.sleep(.5)
                robot.moveForward(int(s['value']))
                time.sleep(int(s['time']))
                robot.moveForward(6000)
            if s['command'] == "turn":
                robot.moveForward(6000)
                time.sleep(.5)
                if int(s['value']) < 6000:
                    robot.turnRight(int(s['value']))
                else:
                    robot.turnLeft(int(s['value']))
                time.sleep(int(s['time']))
                robot.resetRobot()
            if s['command'] == "headtilt":
                print("tilthead")
                robot.resetRobot()
                robot.tiltHeadUp(int(s['value']))
                time.sleep(int(s['time']))
                #robot.resetRobot()
            if s['command'] == "headturn":
                print("turnhead")
                robot.resetRobot()
                robot.turnHeadRight(int(s['value']))
                time.sleep(int(s['time']))
            if s['command'] == "bodyturn":
                robot.resetRobot()
                robot.twistWasteLeft(int(s['value']))
                time.sleep(int(s['time']))
            if s['command'] == "keyboard":
                robot.speak()
            if s["command"] == "speech":
                robot.listen()


            






gui = Gui()
