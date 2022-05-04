# THIS IS THE FRONT END DRIVER...FRONT END WILL MAKE CALLS TO BACK END
# BEGUN: 2022-3-17

# This code will be utilized to anonomize dicom dite in compliance with various Entrepot studies.

# This code creates a user interface for a DicomDeidentify app and calls (insert backend file here)
# to do the processing.

# This code will be package inside a singularity container to be run by a user.

# ver 0.1 begun: 2022-3-17

# author: Daniel G. Balentine, Athinoula A. Martinos Center for Biomedical Imaging, dbalentine@mgh.harvard.edu

"""
    author: Daniel G. Balentine, Martinos Center for Biomedical Imaging, Massachusetts General Hospital
    email: dbalentine@mgh.harvard.edu (2022)

    Started class structure from tutorial (https://pythonprogramming.net/object-oriented-programming-crash-course-tkinter/)

    Page development and layout in Figma and Tkinter code exportation through Proxlight
    Figma: https://www.figma.com/
    Proxlight: https://proxlight.github.io/


"""


import tkinter as tk
from tkinter import ttk
import time
from PIL import ImageTk, Image




LARGE_FONT = ("Verdana", 12)

#see if you can make in a main thats a very linear
#if you are jumping around modules the workflow
#karls reference code https://github.com/TRANSFORM-DBS/MarkVCID/blob/master/data_recording/recordDICOMzip.0.2.py
#karl has a good logger in his program^
#log into markvcid imaging and look at the logfile


class DicomDeidentifyapp(tk.Tk):
    """
        User Interface for DicomDeidentify application.
    """

    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #set overall window size (in Pixels)
        self.geometry("900x900")

        #initialize left corner icon and left corner app title
        tk.Tk.iconbitmap(self, default="images/ddicon.ico")
        tk.Tk.wm_title(self, "DICOM DEIDENTIFY")

        #initialize each container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #initialize dictionary to store each frame object
        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")


        #show start page on app initialization
        self.show_frame(StartPage)

    #method to show a certain page (cont is the page)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


#you want start page to have the browse files button.
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)




        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = ttk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()




class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        # initialize...self is a frame
        tk.Frame.__init__(self, parent)

        # define global image variables so garbage dump doesnt throw them out "https://stackoverflow.com/questions/16424091/why-does-tkinter-image-not-show-up-if-created-in-a-function"
        global background_img
        global img0
        global img1
        global entry0_img
        global entry1_img
        global entry2_img

        # import images to global...
        background_img = tk.PhotoImage(file=f"images/page_1/background.png")
        img0 = tk.PhotoImage(file="images/page_1/img0.png")
        img1 = tk.PhotoImage(file="images/page_1/img1.png")
        entry0_img = tk.PhotoImage(file=f"images/page_1/img_textBox0.png")
        entry1_img = tk.PhotoImage(file=f"images/page_1/img_textBox1.png")
        entry2_img = tk.PhotoImage(file=f"images/page_1/img_textBox2.png")

        #you may want to define canvas as a self object
        # define a canvas to place widgets
        self.canvas = tk.Canvas(self, width=900,
                           height=900,
                           bg="#ffffff",
                           bd=0,
                           highlightthickness=0,
                           relief="ridge")
        # place the canvas in upper left corner of the frame
        self.canvas.place(x=0, y=0)

        # create background image
        background = self.canvas.create_image(140, 448, image=background_img)

        # create entry widget for Patient ID
        entry0_bg = self.canvas.create_image(
            559.0, 215.5,
            image=entry0_img)
        entry0 = tk.Entry(self.canvas,
                          bd=0,
                          bg="#ffffff",
                          highlightthickness=0)
        entry0.place(
            x=458.0, y=195,
            width=202.0,
            height=39)

        # create entry widget for scan session ID
        entry1_bg = self.canvas.create_image(
            559.0, 309.5,
            image=entry1_img)
        entry1 = tk.Entry(self.canvas,
                          bd=0,
                          bg="#ffffff",
                          highlightthickness=0)
        entry1.place(
            x=458.0, y=289,
            width=202.0,
            height=39)

        # create entry widget for Patient ID
        entry2_bg = self.canvas.create_image(
            559.0, 121.5,
            image=entry2_img)
        entry2 = tk.Entry(self.canvas,
                          bd=0,
                          bg="#ffffff",
                          highlightthickness=0)
        entry2.place(
            x=458.0, y=101,
            width=202.0,
            height=39)

        # Create a continue button Widget...could make this a ttk button possibly
        b0 = tk.Button(self.canvas,
                       image=img0,
                       borderwidth=0,
                       highlightthickness=0,
                       command=lambda: controller.show_frame(StartPage),
                       relief="flat")
        b0.place(
            x=464, y=438,
            width=190,
            height=61)

        b1 = tk.Button(self.canvas,
            image=img1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: controller.show_frame(StartPage),
            relief="flat")

        b1.place(
            x=506, y=827,
            width=105,
            height=50)


    def progressbar(self):
        canvas = self.canvas
        #558.5 is inline with the center of buttons and entry boxes, subtract half of the width and you get X dimension to keep it inline
        self.bar = ttk.Progressbar(canvas, orient=tk.HORIZONTAL, length = 300, mode='indeterminate')
        self.bar.place(x=408.5, y = 625)

    def startbar(self):
        self.bar.start(10)

    def stopbar(self):
        self.bar.stop()






class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #define new globals...you have to make all new vars unfortunately...if you reuse it will just take the image from the first page class called.
        #you can reuse variables that aren't globals though
        global background_img_2
        global img0_2

        background_img_2 = tk.PhotoImage(file=f"images/page_2/background.png")
        img0_2 = tk.PhotoImage(file="images/page_2/img0.png")

        # define a canvas to place widgets
        canvas = tk.Canvas(self, width=900,
                           height=900,
                           bg="#ffffff",
                           bd=0,
                           highlightthickness=0,
                           relief="ridge")
        # place the canvas in upper left corner of the frame
        canvas.place(x=0, y=0)

        # create background image
        background = canvas.create_image(450, 450, image=background_img_2)

        # Create a continue button Widget...could make this a ttk button possibly
        b0 = tk.Button(canvas,
                       image=img0_2,
                       borderwidth=0,
                       highlightthickness=0,
                       command=lambda: controller.show_frame(StartPage),
                       relief="flat")
        b0.place(
            x=294, y=542,
            width=312,
            height=88)


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


def main():
    app = DicomDeidentifyapp()
    app.mainloop()
    PageOne.progressbar()
    PageOne.startbar()

if __name__ == "__main__":
    main()






