from tkinter import *
from time import sleep





class LoadingSplash:

        def __init__(self):
            self.root = Tk()
            self.root.config(bg = "#ffffff")
            self.root.title("Loading Page")
            self.root.geometry("900x900")
            canvas = Canvas(
                self.root,
                bg="#ffffff",
                height=900,
                width=900,
                bd=0,
                highlightthickness=0,
                relief="ridge")
            canvas.place(x=0, y=0)
            background_img = PhotoImage(file=f"background.png")
            background = canvas.create_image(
                450.0, 450.0,
                image=background_img)


            #loading blocks:
            for i in range(16):
                Label(self.root, bg="#1F2732", width=2, height=1).place(x=((i + 250) + (i * 22)), y=500)







            #update root to see animation
            self.root.update()
            self.play_animation()

            # window in mainloop
            self.root.mainloop()


        #you need to figure out how to destroy the labels...you cant just keep placing labels on top of one another
        def play_animation(self):
            for i in range(200):
                print(i)
                for j in range(16):

                    #make blocks light
                    label1 = Label(self.root, bg="#BCD7EC", width=2, height=1)
                    label1.place(x=((j + 250) + (j * 22)), y=500)
                    sleep(0.06)
                    self.root.update_idletasks()

                    #make block dark
                    label2 = Label(self.root, bg="#1F2732", width=2, height=1).place(x=((j + 250) + (j * 22)), y=500)
                    label1.destroy()






if __name__ == "__main__":
    LoadingSplash()