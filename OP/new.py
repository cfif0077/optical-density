from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageOps
import os

root = Tk()  # Создание окна
root.title("OP")
root.geometry("640x640")

class Photo:
    def out(self):
        self.image_resize = self.image.resize((600, 420), Image.Resampling.LANCZOS)
        self.image_out = ImageTk.PhotoImage(self.image_resize)
        canvas2.create_image(300, 210, image=self.image_out) #положение фото
        canvas2.image = self.image_out

    def select(self):
        self.path = filedialog.askopenfilename(initialdir=os.getcwd())
        self.image = Image.open(self.path)
        self.out()

    def save(self):
        ext = self.path.split(".")[-1]
        file = asksaveasfilename(defaultextension=f".{ext}", filetypes=[("All Files", "*.*")])
        self.image.save(file)


photo = Photo()

def b3(event):
    rgb = photo.image_resize.getpixel((event.x, event.y))
    print(event.x, event.y)
    print(rgb)
    canvas3['bg'] = '#%02x%02x%02x' % rgb


root.bind('<Button-3>', b3)

frame_photo = Frame(root)
frame_setting = Frame(root)
frame_photo.pack(fill=BOTH)
frame_setting.pack()

btn1 = Button(frame_setting, text="Выбор фото", width=12, font=('ariel 15 bold'), command=photo.select)
btn1.pack(side=LEFT)

btn2 = Button(frame_setting, text="Сохранение", width=12, font=('ariel 15 bold'), command=photo.save)
btn2.pack(side=LEFT)

btn3 = Button(frame_setting, text="Выход", width=12, font=('ariel 15 bold'), command=root.destroy)
btn3.pack(side=LEFT)

canvas2 = Canvas(frame_photo, width=600, height=420,bg="red")
canvas2.pack(fill=BOTH,side=TOP)

canvas3 = Canvas(frame_setting, width="40", height="40", relief=RIDGE, bd=2)
canvas3.pack(side=LEFT)

root.mainloop()