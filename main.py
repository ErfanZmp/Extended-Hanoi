import customtkinter
import models
import hanoi
from hanoi import ExHanoi
import threading

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

HEIGHT = 650
WIDTH = 750
SPEED = 10

def fill_towers(n, canvas ,towers):
    counter = n*3
    for _ in range(n, 0, -1):
        for i in range(3):
                models.Disk(canvas, towers[i], counter)
                counter -= 1

def wait_to_finish(self):
    self.thread.join()
    self.running = False
    self.finished = True
    self.title.configure(text=f"Finished", fg="white")
    self.resume_bt.configure(text="Start")

def reset_towers(self):
    if self.running and self.started:
        self.title.configure(text="Please Pause Before Reset", fg="red")
        return
    print("Reseting...")
    models.RESET = True
    self.running = False
    self.started = False
    self.finished = False
    self.canvas.delete("disk_tag")
    self.towerA.clear()
    self.towerB.clear()
    self.towerC.clear()
    fill_towers(self.disk_num, self.canvas, [self.towerA, self.towerB, self.towerC])
    self.resume_bt.configure(text="Start")  
    self.title.configure(text=f"Disks: {self.disk_num}", fg="white")
    hanoi.move = models.Move()
    print("Reset Done.")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Extended Hanoi Problem")
        self.minsize(WIDTH, HEIGHT)

        self.frame = HomeFrame(master=self)
        self.frame.pack(padx=20, pady=60, fill="both", expand=True)

    def go_main(self, n):
        self.frame.destroy()
        self.frame = MainFrame(master=self, disks=n)
        self.frame.pack(padx=20, pady=60, fill="both", expand=True)

    def go_home(self):
        self.frame.destroy()
        self.frame = HomeFrame(master=self)
        self.frame.pack(padx=20, pady=60, fill="both", expand=True)

class HomeFrame(customtkinter.CTkFrame):
    def __init__(self, master: App):
        super().__init__(master)

        self.master_app = master

        self.wlc_label = customtkinter.CTkLabel(master=self, text="Welcome!")
        self.wlc_label.configure(font=('Helvetica bold', 26))
        self.wlc_label.pack(padx=12, pady=12)

        self.inp_label = customtkinter.CTkLabel(master=self, text="Choose the number of disks")
        self.inp_label.configure(font=('Helvetica', 20))
        self.inp_label.pack(padx=12)

        self.inp_frame = customtkinter.CTkFrame(master=self)
        self.inp_frame.pack(padx=12, pady=12)

        self.combobox = customtkinter.CTkOptionMenu(master=self.inp_frame, values=[str(i+1) for i in range(10)])
        self.combobox.pack(padx=12, pady=10, side='left')

        self.button = customtkinter.CTkButton(master=self.inp_frame, command=self.button_callback, text="Run")
        self.button.pack(padx=12, pady=10, side='right')

        self.exit = customtkinter.CTkButton(master=self, command=quit, text="Exit")
        self.exit.pack(padx=12, pady=10)

    def button_callback(self):
        self.master_app.go_main(self.combobox.get())

class MainFrame(customtkinter.CTkFrame):

    def __init__(self, master: App, disks):
        super().__init__(master)
        
        self.started = False
        self.finished = False
        self.running = False
        self.disk_num = int(disks)

        self.title = customtkinter.CTkLabel(master=self, text=f"Disks: {self.disk_num}")
        self.title.configure(font=('Helvetica', 20))
        self.title.pack(padx=12, pady=12)

        self.c_width, self.c_height = 500, 300
        self.canvas = customtkinter.CTkCanvas(master=self, width=self.c_width, height=self.c_height)
        self.canvas.pack(padx=10, pady=12)

        self.x1 = 80
        self.x2 = 235
        self.x3 = 390
        self.y = 50
        self.t_height, self.t_width = 220, 30

        self.towerA = models.Tower(self.canvas, self.x1, self.y, self.t_width, self.t_height, "A")
        self.towerB = models.Tower(self.canvas, self.x2, self.y, self.t_width, self.t_height, "B")
        self.towerC = models.Tower(self.canvas, self.x3, self.y, self.t_width, self.t_height, "C")

        fill_towers(self.disk_num, self.canvas, [self.towerA, self.towerB, self.towerC])

        self.option_frame = customtkinter.CTkFrame(master=self, border_color="#858585")
        self.option_frame.pack(padx=8, pady=8)

        self.slide_frame = customtkinter.CTkFrame(master=self.option_frame)
        self.slide_frame.pack(padx=6, pady=6, fill="both", expand=True)

        self.speed_label = customtkinter.CTkLabel(master=self.slide_frame, text="Speed", width=110, text_color="#858585")
        self.speed_label.configure(font=('Helvetica', 16))
        self.speed_label.pack(padx=12, pady=12, side='left')

        self.slider = customtkinter.CTkSlider(master=self.slide_frame, command=self.change_speed, from_=1, to=25, width=340)
        self.slider.pack(padx=8, pady=8, side='right')

        self.resume_bt = customtkinter.CTkButton(master=self.option_frame, command=self.start, text="Start")
        self.resume_bt.pack(padx=12, pady=12, side='left')

        self.pause = customtkinter.CTkButton(master=self.option_frame, command=self.reset, text="Reset")
        self.pause.pack(padx=12, pady=12, side='left')

        self.back = customtkinter.CTkButton(master=self.option_frame, command=self.home , text="Back")
        self.back.pack(padx=12, pady=12, side='right')
    
    def home(self):
        hanoi.move.pause()
        hanoi.move = models.Move()
        self.master.go_home()

    def start(self):
        if self.finished:
            threading.Thread(target=reset_towers, args=(self,)).start()
        if self.started:
            if self.running:
                hanoi.move.pause()
                print("Paused")
                self.title.configure(text=f"Paused", fg="yellow")
                self.resume_bt.configure(text="Resume")
                self.running = False
            else:
                hanoi.move.resume()
                print("Resumed")
                self.title.configure(text=f"Running", fg="Green")
                self.resume_bt.configure(text="Pause")
                self.running = True
        else:
            models.RESET = False
            self.resume_bt.configure(text="Pause")
            self.thread = threading.Thread(target=ExHanoi, args=(self.towerA, self.towerB, self.towerC, self.disk_num))
            self.thread.start()
            threading.Thread(target=wait_to_finish, args=(self,)).start()
            self.title.configure(text=f"Running", fg="Green")
            self.started = True
            self.running = True
    
    def reset(self):
        threading.Thread(target=reset_towers, args=(self,)).start()

    def change_speed(self, value):
        models.SPEED = int(value)
        

if __name__ == "__main__":
    app = App()
    app.mainloop()