from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from PIL import Image, ImageTk, ImageEnhance
import os
from numpy import asarray

class Photo:
    def __init__(self):
        self.flag = False
        self.size = (640, 420)

    def out(self):
        self.flag = True
        self.image_resize = self.image.resize(self.size, Image.Resampling.LANCZOS)
        self.image_out = ImageTk.PhotoImage(self.image_resize)
        canvas2.delete("IMG")
        canvas2.create_image(0, 0, anchor=NW, image=self.image_out, tags="IMG")

    def select(self):
        self.path = filedialog.askopenfilename(initialdir=os.getcwd())
        self.image_clean = Image.open(self.path)
        self.image = self.image_clean
        self.out()

    def save(self):
        ext = self.path.split(".")[-1]
        file = asksaveasfilename(defaultextension=f".{ext}", filetypes=[("All Files", "*.*")])
        self.image.save(file)

    def resize(self, size=(640, 420)):
        if self.flag:
            if size != (640, 420):
                self.size = size
            self.out()

    def test(self,event):
        # split the image into individual bands
        source = self.image_clean.split()
        R, G, B = 0, 1, 2
        # select regions where red is less than 200
        razm = v1.get()
        mask_r = source[R].point(lambda i: -razm <= i - self.rgb[R] <= razm and 255)
        mask_g = source[G].point(lambda i: -razm <= i - self.rgb[G] <= razm and 255)
        mask_b = source[B].point(lambda i: -razm <= i - self.rgb[B] <= razm and 255)
        mask_all = asarray(mask_r)*asarray(mask_g)*asarray(mask_b)
        # process the green band
        out = source[G].point(lambda i: i * 2)
        # paste the processed band back, but only where red was < 100
        source[G].paste(out, None, Image.fromarray(mask_all))
        #print(asarray(source[G]))
        # build a new multiband image
        self.image = Image.merge(self.image.mode, source)
        self.resize()

    def test1(self):
        self.image = self.image_clean
        self.resize()

    def brightness(self,event):
        imgg = ImageEnhance.Brightness(self.image_clean)
        self.image = imgg.enhance(var_bright.get() + 1)
        self.out()

    def contrast(self,event):
        imgg = ImageEnhance.Contrast(self.image_clean)
        self.image = imgg.enhance(var_contrast.get() + 1)
        self.out()

def b3(event):
    photo.rgb = photo.image_resize.getpixel((event.x, event.y))
    print(photo.rgb)
    canvas3['bg'] = '#%02x%02x%02x' % photo.rgb

def resize(event):
    photo.resize((event.width, event.height))

photo = Photo()

root = Tk()  # Создание окна
root.title("OP")
root.geometry("640x560")

frame_photo = Frame(root)
frame_photo.pack(fill=BOTH, expand=True)

frame_setting = Frame(root)
frame_setting.pack(fill=Y)

frame_setting_photo = Frame(root)
frame_setting_photo.pack(fill=Y)

frame_setting_calculat = Frame(root)
frame_setting_calculat.pack(fill=Y)


#окно с фото
canvas2 = Canvas(frame_photo, width=600, height=420)
canvas2.pack(fill=BOTH, expand=1)


#окно настроек выбора
btn_select = Button(frame_setting, text="Выбор фото", width=12, font=('ariel 15 bold'), command=photo.select)
btn_select.pack(side=LEFT)

btn_save = Button(frame_setting, text="Сохранение", width=12, font=('ariel 15 bold'), command=photo.save)
btn_save.pack(side=LEFT)

btn_exit = Button(frame_setting, text="Выход", width=6, font=('ariel 15 bold'), command=root.destroy)
btn_exit.pack(side=LEFT)

#окно настрое фото
#яркость
bright = Label(frame_setting_photo, text="Яркость:", font=("ariel 15 bold"))
bright.pack(side=LEFT)
var_bright = IntVar()
scale_bright = Scale(frame_setting_photo, from_=0, to=10, variable=var_bright, orient=HORIZONTAL, command=photo.brightness)
scale_bright.pack(side=LEFT)

#Контрастность
contrast = Label(frame_setting_photo, text="Контраст:", font=("ariel 17 bold"))
contrast.pack(side=LEFT)
var_contrast = IntVar()
scale_contrast = Scale(frame_setting_photo, from_=0, to=10, variable=var_contrast, orient=HORIZONTAL, command=photo.contrast)
scale_contrast.pack(side=LEFT)


#окно настроек счета
def checkbutton_changed(event=0):
    if enabled.get() == 1:
        photo.test(event)
    else:
        photo.test1()

enabled = IntVar()
btn4 = Checkbutton(frame_setting_calculat, text="Проверка", width=8, font=('ariel 15 bold'), variable=enabled, command=checkbutton_changed)
btn4.pack(side=LEFT)

v1 = IntVar()
scale3 = Scale(frame_setting_calculat, from_=0, to=40, variable=v1, orient=HORIZONTAL, command=checkbutton_changed)
scale3.pack(side=LEFT)

canvas3 = Canvas(frame_setting_calculat, width="40", height="40", relief=RIDGE, bd=2)
canvas3.pack(side=LEFT)


main_menu = Menu()

file_menu = Menu(font=("Verdana", 11, "bold"), tearoff=0)
file_menu.add_command(label="Открыть", command=photo.select)
file_menu.add_command(label="Сохранить", command=photo.save)
file_menu.add_separator()
file_menu.add_command(label="Выход", command=root.destroy)

def help_click():
    messagebox.showinfo("Тех. поддержка", "89119659493\n Александр")

main_menu.add_cascade(label="File", menu=file_menu)
main_menu.add_cascade(label="Тех. поддержка", command=help_click)

root.config(menu=main_menu)

root.bind('<Button-3>', b3)
root.bind("<Configure>", resize)

root.mainloop()
