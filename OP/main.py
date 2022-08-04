from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from PIL import Image, ImageTk
import os


class Photo:
    def __init__(self):
        self.flag = False

    def out(self):
        self.flag = True
        self.image_resize = self.image.resize((640, 420), Image.Resampling.LANCZOS)
        self.image_out = ImageTk.PhotoImage(self.image_resize)
        canvas2.create_image(0, 0, anchor=NW, image=self.image_out, tags="IMG")

    def select(self):
        self.path = filedialog.askopenfilename(initialdir=os.getcwd())
        self.image = Image.open(self.path)
        self.out()

    def save(self):
        ext = self.path.split(".")[-1]
        file = asksaveasfilename(defaultextension=f".{ext}", filetypes=[("All Files", "*.*")])
        self.image.save(file)

    def resize(self, size):
        if self.flag:
            self.image_resize = self.image.resize(size, Image.Resampling.LANCZOS)
            self.image_out = ImageTk.PhotoImage(self.image_resize)
            canvas2.delete("IMG")
            canvas2.create_image(0, 0, image=self.image_out, anchor=NW, tags="IMG")

def b3(event):
    rgb = photo.image_resize.getpixel((event.x, event.y))
    print(event.x, event.y)
    canvas3['bg'] = '#%02x%02x%02x' % rgb

def resize(event):
    photo.resize((event.width, event.height))

photo = Photo()

root = Tk()  # Создание окна
root.title("OP")
root.geometry("640x460")

frame_photo = Frame(root)
frame_setting = Frame(root)
frame_photo.pack(fill=BOTH, expand=True)
frame_setting.pack(fill=Y)

btn1 = Button(frame_setting, text="Выбор фото", width=12, font=('ariel 15 bold'), command=photo.select)
btn1.pack(side=LEFT)

btn2 = Button(frame_setting, text="Сохранение", width=12, font=('ariel 15 bold'), command=photo.save)
btn2.pack(side=LEFT)

btn3 = Button(frame_setting, text="Выход", width=12, font=('ariel 15 bold'), command=root.destroy)
btn3.pack(side=LEFT)

canvas2 = Canvas(frame_photo, width=600, height=420)
canvas2.pack(fill=BOTH, expand=1)

canvas3 = Canvas(frame_setting, width="40", height="40", relief=RIDGE, bd=2)
canvas3.pack(side=LEFT)

main_menu = Menu()

file_menu = Menu(font=("Verdana", 11, "bold"), tearoff=0)
file_menu.add_command(label="Открыть", command=photo.select)
file_menu.add_command(label="Сохранить", command=photo.save)
file_menu.add_separator()
file_menu.add_command(label="Выход", command=root.destroy)

def help_click():
    messagebox.showinfo("GUI Python", "89119659493\n Александр")

main_menu.add_cascade(label="File", menu=file_menu)
main_menu.add_cascade(label="Тех. поддержка", command=help_click)

root.config(menu=main_menu)

root.bind('<Button-3>', b3)
root.bind("<Configure>", resize)

root.mainloop()
