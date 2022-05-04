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

    4/15/2022 - Converted to Pep-8 style.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.font import Font
from threading import Thread
import backend as back
import logger


# user interface class for application
class DicomDeidentifyApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.log = logger.log_module()
        
        # set overall window size (in Pixels)
        self.geometry("900x810")

        # initialize left corner icon and left corner app title
        tk.Tk.iconbitmap(self, default="images/ddicon.ico")
        tk.Tk.wm_title(self, "DICOM DEIDENTIFY")

        # color theme in hex
        self.blue_light = '#BCD7EC'
        self.blue_extra_light = '#DBEAF0'
        self.blue_dark = '#80ADC4'
        self.blue_extra_dark = '#143748'
        self.back_color = '#030102'
        self.red_light = '#FEC3C3'

        # font defined
        self.Main_Font = Font(family="Montseratt", size=18)

    def page_one(self):
        # log start page
        self.log.logger.info("Start page has begun initialization...")

        # create and place a frame
        frame = tk.Frame(self)
        frame.place(x=0,y=0)

        # import images...
        self.BACKGROUND_IMG = tk.PhotoImage(file=f"images/page_1/background.png")
        self.BROWSE_FILES_IMG = tk.PhotoImage(file="images/page_1/browse_files.png")
        self.ENTRY0_IMG = tk.PhotoImage(file=f"images/page_1/img_textBox0.png")
        self.ENTRY1_IMG = tk.PhotoImage(file=f"images/page_1/img_textBox1.png")
        self.ENTRY2_IMG = tk.PhotoImage(file=f"images/page_1/img_textBox2.png")
        self.START_IMG = tk.PhotoImage(file=f"images/page_1/start.png")
        self.RESTART_PROG_IMG = tk.PhotoImage(file=f"images/page_1/restart_program.png")
        self.CLOSE_BUTTON_IMG = tk.PhotoImage(file=f"images/page_1/close_button.png")
        self.CLEAR_BUTTON_IMG = tk.PhotoImage(file=f"images/page_1/clear_button.png")

        # define a canvas to place widgets
        self.canvas = tk.Canvas(self, width=900,
                                height=810,
                                bg="#ffffff",
                                bd=0,
                                highlightthickness=0,
                                relief="ridge")
        # place the canvas in upper left corner of the frame
        self.canvas.place(x=0, y=0)

        # create canvas background image
        background = self.canvas.create_image(116.5, 357.0, image=self.BACKGROUND_IMG)

        # create entry widget and label for Patient ID
        self.patientID_label = tk.Label(self.canvas,
                                        text ="Participant ID",
                                        font=self.Main_Font,
                                        foreground=self.blue_light,
                                        background = self.back_color)
        self.patientID_label.place(x=597,y=301, anchor = 'center')
        entry0_bg = self.canvas.create_image(
            597.0, 336.5,
            image=self.ENTRY0_IMG)
        self.entryPatientID = tk.Entry(self.canvas,
                          bd=0,
                          bg="#ffffff",
                          highlightthickness=0)
        self.entryPatientID.place(
            x=496.0, y=316,
            width=202.0,
            height=39)

        # create entry widget and label for scan session ID
        self.scan_session_ID_label = tk.Label(self.canvas, text="Scan Session ID", font=self.Main_Font, foreground=self.blue_light,
                                        background=self.back_color)
        self.scan_session_ID_label.place(x=597, y=402, anchor='center')
        entry1_bg = self.canvas.create_image(
            597.0, 433.5,
            image=self.ENTRY1_IMG)
        self.entryScanSessionID = tk.Entry(self.canvas,
                          bd=0,
                          bg="#ffffff",
                          highlightthickness=0)
        self.entryScanSessionID.place(
            x=496.0, y=413,
            width=202.0,
            height=39)

        # create entry widget for Site ID
        self.site_ID_label = tk.Label(self.canvas, text="Site ID", font=self.Main_Font, foreground=self.blue_light,
                                        background=self.back_color)
        self.site_ID_label.place(x=597, y=203, anchor='center')
        entry2_bg = self.canvas.create_image(
            597.0, 239.5,
            image=self.ENTRY2_IMG)
        self.entrySiteID = tk.Entry(self.canvas,
                          bd=0,
                          bg="#ffffff",
                          highlightthickness=0)
        self.entrySiteID.place(x=496.0, y=219,
                            width=202.0,
                            height=39)

        # create the "Please select the files to be deidentified" text.
        self.select_files_label = tk.Label(self.canvas, text="Please select the files to be deidentified.", font=self.Main_Font, foreground=self.blue_light,
                                        background=self.back_color)
        self.select_files_label.place(x=597, y=507, anchor='center')

        # create a continue button Widget...could make this a ttk button possibly
        self.browse_button = tk.Button(self.canvas,
                       image=self.BROWSE_FILES_IMG,
                       borderwidth=0,
                       highlightthickness=0,
                       command=lambda: self.browse_files(),
                       relief="flat")
        self.browse_button.place(
            x=502, y=547,
            width=190,
            height=61)

        # create the start program button
        self.start_button = tk.Button(self.canvas,
                                      image=self.START_IMG,
                                      borderwidth=0,
                                      highlightthickness=0,
                                      command=lambda: self.get_entry(),
                                      relief="flat")
        # create the restart button
        self.restart_button = tk.Button(self.canvas,
                                    image=self.RESTART_PROG_IMG,
                                    borderwidth=0,
                                    highlightthickness=0,
                                    command=lambda: self.restart_app(),
                                    relief="flat")

        # create and place the close button
        self.close_button = tk.Button(self.canvas,
            image= self.CLOSE_BUTTON_IMG,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: exit(),
            relief="flat")
        self.close_button.place(
            x=866, y=4,
            width=30,
            height=30)

        #clear button
        self.clear_button = tk.Button(self.canvas,
                                      image= self.CLEAR_BUTTON_IMG,
                                      borderwidth=0,
                                      highlightthickness=0,
                                      command=lambda: self.restart_app(),
                                      relief="flat")
        self.log.logger.info("Start page has been initialized")
        #raise frame to window
        frame.tkraise()

    def browse_files(self):
        self.log.logger.info("Browse files button clicked")
        self.path = filedialog.askdirectory()
        self.browse_button.destroy()
        self.select_files_label.destroy()
        # start button calls get entry
        self.start_button.place(
            x=502, y=547,
            width=190,
            height=61)

    def get_entry(self):
        self.log.logger.info("Start button clicked")
        self.patientID = self.entryPatientID.get()
        self.scansessionID = self.entryScanSessionID.get()
        self.siteID = self.entrySiteID.get()
        self.check_entry()

    def popup(self,text):
        popup = tk.Label(self.canvas,text = text, font=('Montseratt',24), foreground=self.red_light, background = self.back_color)
        popup.place(x=597, y=507, anchor = "center")
        self.after(2000,popup.destroy)

    def check_entry(self):
        #store all valid site ID
        markvcid_site_ID = [602,603,604,605,606,607,608,609,617,618,622,633,635,
                           650,651]
        discovery_site_ID = [612,617,618,610,634,622,613,627,628,629,631,632,637,
                            611,638,620,615,625,633,635,636,616,639,630,626,614,624,640,641]
        site_ID_bank = markvcid_site_ID + discovery_site_ID
        site_ID_bank = list(map(str,site_ID_bank))

        #entry quality check
        if len(self.siteID) == 3 and \
                self.siteID in site_ID_bank and \
                len(self.patientID) and \
                len(self.scansessionID) == 32:
            self.run_backend()
        elif len(self.siteID) != 3:
            self.popup("Site ID of Incorrect Length")
        elif self.siteID not in site_ID_bank:
            self.popup("Site ID Invalid")
        elif len(self.patientID) != 10:
            self.popup("Patient ID of Incorrect Length")
        elif len(self.scansessionID) != 32:
            self.popup("Scan Session ID of Incorrect Length")

    def run_backend(self):
        # run progress bar
        self.start_progress_bar()

        # a results list is created to get any info from backend. Passed into our back.run function as an arg.
        self.thread_results = []

        # using threading so GUI is still responsive while backend runs
        # parent used to show this is front_end running, needed for unit tests
        parent = 'front_end'
        thread1 = Thread(target=back.run, args=[self.path,self.siteID,self.patientID,self.scansessionID,self.thread_results,self.log, parent])
        thread1.start()
        # monitor if thread1 is still running
        self.monitor_thread(thread1)

    def monitor_thread(self,thread):
        if thread.is_alive():
            # check the thread every 100ms
            self.after(100, lambda: self.monitor_thread(thread))
        else:
            self.stop_progress_bar()

    def start_progress_bar(self):
        #destroy start and reselct files buttons
        self.start_button.destroy()

        #progress bar
        self.bar_style = ttk.Style()
        self.bar_style.theme_use('clam')
        self.bar_style.configure("red.Horizontal.TProgressbar", foreground ='red', background= self.blue_light, troughcolor = self.blue_extra_dark, bordercolor= self.blue_extra_dark)
        self.bar = ttk.Progressbar(self.canvas,style="red.Horizontal.TProgressbar",orient=tk.HORIZONTAL, length=300, mode='indeterminate')
        self.bar.place(x=447, y=625)
        self.bar.start(10)

    def stop_progress_bar(self):
        self.bar.stop()
        self.bar.destroy()
        self.backend_completion()

    def backend_completion(self):
        self.num_of_files = self.thread_results[0]
        self.completed_frame()

    def completed_frame(self):
        # position inline with all buttons and entries is 559.0
        self.num_of_files_label = tk.Label(self.canvas,text ="Congrats! You have deidentified {} files.".format(self.num_of_files), font=('Montseratt',18), foreground=self.blue_light, background = self.back_color)
        self.num_of_files_label.place(x=597, y=557,anchor="center")

        # place clear button (clear button calls restart app)
        self.clear_button.place(
            x=597, y=650,
            width=101,
            height=61,
            anchor = "center")

        """"
        self.path_label = tk.Label(self.canvas,text ="Your files are located in {}".format(self.path), font=('Montseratt',8), foreground=self.blue_light, background = self.back_color)
        self.path_label.place(x=559.0,y=700,anchor="center")
        """

    def restart_app(self):
        self.log.logger.info("Program has been restarted")
        #delete entries and path
        del self.siteID, self.patientID, self.scansessionID, self.path, self.thread_results

        #destroy restart and exit buttons
        self.restart_button.destroy()

        #clear entries of text
        self.entrySiteID.delete(0, 'end')
        self.entryPatientID.delete(0,'end')
        self.entryScanSessionID.delete(0,'end')

        #initialize page one again
        self.page_one()


def main():
    app = DicomDeidentifyApp()
    app.page_one()
    app.mainloop()

if __name__ == "__main__":
    main()