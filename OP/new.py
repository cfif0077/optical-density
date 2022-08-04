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

btn1 = Button(root, text="Выбор фото", width=12, font=('ariel 15 bold'), command=photo.select)
btn1.place(x=50, y=595)

btn2 = Button(root, text="Сохранение", width=12, font=('ariel 15 bold'), command=photo.save)
btn2.place(x=240, y=595)

btn3 = Button(root, text="Выход", width=12, font=('ariel 15 bold'), command=root.destroy)
btn3.place(x=450, y=595)

canvas2 = Canvas(root, width="600", height="420")
canvas2.place(x=0, y=0)

canvas3 = Canvas(root, width="40", height="40", relief=RIDGE, bd=2)
canvas3.place(x=550, y=450)

root.mainloop()