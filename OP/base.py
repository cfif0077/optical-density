from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageOps
import os

# создание окна
root = Tk()  # Create a window
root.title("Оптическая плотность")  # Set the title of the window
root.geometry("640x640")  # Set the size of the window

#выбор фото
def select():
    global img_path, img
    img_path = filedialog.askopenfilename(initialdir=os.getcwd())
    img = Image.open(img_path)
    img.thumbnail((350, 350))
    img1 = ImageTk.PhotoImage(img)
    canvas2.create_image(300, 210, image=img1)
    canvas2.image = img1

#блюр эффект
def blur(event):
    global img_path, img1, imgg
    for m in range(0, v1.get()+1):
        img = Image.open(img_path)
        img.thumbnail((350, 350))
        imgg = img.filter(ImageFilter.BoxBlur(m))
        img1 = ImageTk.PhotoImage(imgg)
        canvas2.create_image(300, 210, image=img1)
        canvas2.image = img1

#яркость
def brightness(event):
    global img_path, img2, img3
    for m in range(0, v2.get()+1):
        img = Image.open(img_path)
        img.thumbnail((350, 350))
        imgg = ImageEnhance.Brightness(img)
        img2 = imgg.enhance(m)
        img3 = ImageTk.PhotoImage(img2)
        canvas2.create_image(300, 210, image=img3)
        canvas2.image = img3

#контрастность
def contrast(event):
    global img_path, img4, img5
    for m in range(0, v3.get()+1):
        img = Image.open(img_path)
        img.thumbnail((350, 350))
        imgg = ImageEnhance.Contrast(img)
        img4 = imgg.enhance(m)
        img5 = ImageTk.PhotoImage(img4)
        canvas2.create_image(300, 210, image=img5)
        canvas2.image = img5


def rotate(event):
    global img_path, img6, img7
    img = Image.open(img_path)
    img.thumbnail((350, 350))
    img6 = img.rotate(int(rotate_combo.get()))
    img7 = ImageTk.PhotoImage(img6)
    canvas2.create_image(300, 210, image=img7)
    canvas2.image = img7


def flip(event):
    global img_path, img8, img9
    img = Image.open(img_path)
    img.thumbnail((350, 350))
    if flip_combo.get() == "FLIP LEFT TO RIGHT":
        img8 = img.transpose(Image.FLIP_LEFT_RIGHT)
    elif flip_combo.get() == "FLIP TOP TO BOTTOM":
        img8 = img.transpose(Image.FLIP_TOP_BOTTOM)
    img9 = ImageTk.PhotoImage(img8)
    canvas2.create_image(300, 210, image=img9)
    canvas2.image = img9


def border(event):
    global img_path, img10, img11
    img = Image.open(img_path)
    img.thumbnail((350, 350))
    img10 = ImageOps.expand(img, border=int(border_combo.get()), fill=95)
    img11 = ImageTk.PhotoImage(img10)
    canvas2.create_image(300, 210, image=img11)
    canvas2.image = img11


img1 = None
img3 = None
img5 = None
img7 = None
img9 = None
img11 = None


def save():
    global img_path, imgg, img1, img2, img3, img4, img5, img6, img7, img8, img9, img10, img11
    ext = img_path.split(".")[-1]
    file = asksaveasfilename(defaultextension=f".{ext}", filetypes=[(
        "All Files", "*.*"), ("PNG file", "*.png"), ("jpg file", "*.jpg")])
    if file:
        if canvas2.image == img1:
            imgg.save(file)
        elif canvas2.image == img3:
            img2.save(file)
        elif canvas2.image == img5:
            img4.save(file)
        elif canvas2.image == img7:
            img6.save(file)
        elif canvas2.image == img9:
            img8.save(file)
        elif canvas2.image == img11:
            img10.save(file)

#размытие
blurr = Label(root, text="Размытие:", font=("ariel 17 bold"), width=9, anchor='e')
blurr.place(x=15, y=8)
v1 = IntVar()
scale1 = ttk.Scale(root, from_=0, to=10, variable=v1,
                   orient=HORIZONTAL, command=blur)
scale1.place(x=150, y=10)

#яркость
bright = Label(root, text="Яркость:", font=("ariel 17 bold"))
bright.place(x=35, y=50)
v2 = IntVar()
scale2 = ttk.Scale(root, from_=0, to=10, variable=v2,
                   orient=HORIZONTAL, command=brightness)
scale2.place(x=150, y=55)

#Контрастность
contrast = Label(root, text="Контраст:", font=("ariel 17 bold"))
contrast.place(x=30, y=92)
v3 = IntVar()
scale3 = ttk.Scale(root, from_=0, to=10, variable=v3,
                   orient=HORIZONTAL, command=contrast)
scale3.place(x=150, y=100)

#поворот
rotate = Label(root, text="Поворот:", font=("ariel 17 bold"))
rotate.place(x=370, y=8)
values = [0, 90, 180, 270, 360]
rotate_combo = ttk.Combobox(root, values=values, font=('ariel 10 bold'))
rotate_combo.place(x=460, y=15)
rotate_combo.bind("<<ComboboxSelected>>", rotate)

#Отзеркаливание
flip = Label(root, text="Зеркало:", font=("ariel 17 bold"))
flip.place(x=400, y=50)
values1 = ["FLIP LEFT TO RIGHT", "FLIP TOP TO BOTTOM"]
flip_combo = ttk.Combobox(root, values=values1, font=('ariel 10 bold'))
flip_combo.place(x=460, y=57)
flip_combo.bind("<<ComboboxSelected>>", flip)

#границы
border = Label(root, text="Add border:", font=("ariel 17 bold"))
border.place(x=320, y=92)
values2 = [i for i in range(10, 45, 5)]
border_combo = ttk.Combobox(root, values=values2, font=("ariel 10 bold"))
border_combo.place(x=460, y=99)
border_combo.bind("<<ComboboxSelected>>", border)

# холст изображения
canvas2 = Canvas(root, width="600", height="420", relief=RIDGE, bd=2)
canvas2.place(x=15, y=150)

# кнопки
btn1 = Button(root, text="Выбор фото",  width=12, font=('ariel 15 bold'), command=select)
btn1.place(x=50, y=595)

btn2 = Button(root, text="Сохранение", width=12, font=('ariel 15 bold'), command=save)
btn2.place(x=240, y=595)

btn3 = Button(root, text="Выход", width=12, font=('ariel 15 bold'), command=root.destroy)
btn3.place(x=450, y=595)

btn4 = Button(root, text="оп", width=2, font=('ariel 15 bold'), command=root.destroy)
btn4.place(x=1, y=595)

# Execute Tkinter
root.mainloop()