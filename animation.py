
import tkinter as tk
from PIL import Image



def gifAnimation():
    root = tk.Tk()
    file="./assets/RUN.gif"

    info = Image.open(file)

    frames = info.n_frames  # gives total number of frames that gif contains

    # creating list of PhotoImage objects for each frames
    im = [tk.PhotoImage(file=file,format=f"gif -index {i}") for i in range(frames)]

    count = 0
    anim = None
    def animation(count):
        global anim
        im2 = im[count]

        gif_label.configure(image=im2)
        count += 1
        if count == frames:
            count = 0
        anim = root.after(50,lambda :animation(count))

    gif_label = tk.Label(root,image="")
    gif_label.pack()

    animation(count)



    root.mainloop()


gifAnimation()