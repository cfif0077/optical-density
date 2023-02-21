from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox
from PIL import Image, ImageTk, ImageEnhance, ImageDraw
import os
from numpy import asarray, count_nonzero, shape


class Photo:
    def __init__(self):
        self.flag = False
        self.size = (90, 50)
        self.rgb = None
        self.good_pixel = None
        self.true_good_pixel = None
        self.error_good_pixel = 0
        self.rgb_good_pixel = None
        self.all_pixel = None
        self.true_all_pixel = None
        self.error_all_pixel = 0
        self.rgb_all_pixel =None

    def out(self):
        self.flag = True
        self.image_resize = self.image.resize(self.size)
        self.draw = ImageDraw.Draw(photo.image_resize)
        self.image_clean_resize = self.image_clean.resize(self.size)
        self.image_out = ImageTk.PhotoImage(self.image_resize)
        canvas2.delete("IMG")
        canvas2.create_image(0, 0, anchor=NW, image=self.image_out, tags="IMG")

    def select(self):
        self.path = filedialog.askopenfilename(initialdir=os.getcwd())
        self.image_true_clean = Image.open(self.path)
        self.image_clean = self.image_true_clean
        self.image = self.image_clean
        self.out()

    def save(self):
        ext = self.path.split(".")[-1]
        file = asksaveasfilename(defaultextension=f".{ext}", filetypes=[("All Files", "*.*")])
        self.image.save(file)

    def resize(self, event):
        self.size = (canvas2.winfo_width(), canvas2.winfo_height())
        if self.flag:
            self.out()

    def out_image_clean(self):
        self.image = self.image_clean
        self.out()

    def out_image_not_clean(self):
        source = self.image_clean.split()
        r, g, b = 0, 1, 2
        self.error_good_pixel = v1.get()
        self.rgb_good_pixel = self.rgb
        error = self.error_good_pixel
        mask_r = source[r].point(lambda i: -error <= i - self.rgb[r] <= error and 255)
        mask_g = source[g].point(lambda i: -error <= i - self.rgb[g] <= error and 255)
        mask_b = source[b].point(lambda i: -error <= i - self.rgb[b] <= error and 255)
        mask_all = asarray(mask_r)*asarray(mask_g)*asarray(mask_b)
        # слой с зеленым цветом
        out = source[g].point(lambda i: i * 2)
        # введение зеленого цвета только в нужные места
        source[g].paste(out, None, Image.fromarray(mask_all))
        # построение нового фото
        self.good_pixel = count_nonzero(mask_all)
        self.image = Image.merge(self.image.mode, source)
        self.out()

    def out_image_delete(self):
        source = self.image_clean.split()
        r, g, b = 0, 1, 2
        self.error_all_pixel = v1.get()
        self.rgb_all_pixel = self.rgb
        error = self.error_all_pixel
        mask_r = source[r].point(lambda i: -error <= i - self.rgb[r] <= error and 255)
        mask_g = source[g].point(lambda i: -error <= i - self.rgb[g] <= error and 255)
        mask_b = source[b].point(lambda i: -error <= i - self.rgb[b] <= error and 255)
        mask_all = asarray(mask_r)*asarray(mask_g)*asarray(mask_b)
        # слой с зеленым цветом
        out = source[r].point(lambda i: i * 2)
        # введение зеленого цвета только в нужные места
        source[r].paste(out, None, Image.fromarray(mask_all))
        # построение нового фото
        self.all_pixel = (shape(mask_all)[0]*shape(mask_all)[1])-count_nonzero(mask_all)
        self.image = Image.merge(self.image.mode, source)
        self.out()

    def filter(self, event):
        image_for_brightness = ImageEnhance.Brightness(self.image_true_clean)
        image = image_for_brightness.enhance(var_bright.get() * 0.1 + 1)

        image_for_contrast = ImageEnhance.Contrast(image)
        image = image_for_contrast.enhance(var_contrast.get() * 0.1+1)

        image_for_sharpness = ImageEnhance.Sharpness(image)
        image = image_for_sharpness.enhance(var_sharpness.get() + 1)

        image_for_color_balance = ImageEnhance.Color(image)
        self.image_clean = image_for_color_balance.enhance(var_color_balance.get() * 0.1 + 1)

        radiobutton_changed()

    def scale_change(self, event=1):
        match select_photo_condition.get():
            case "выбрать":
                photo.out_image_not_clean()
            case "исключить":
                photo.out_image_delete()

    def number_point(self):
        size = shape(self.image_clean.split()[0])
        source = self.image_resize.resize(size).split()
        r, g, b = 0, 1, 2
        # счет добавляемых пикселей
        mask_r_black = source[r].point(lambda i: i == 0 and 255)
        mask_g_black = source[g].point(lambda i: i == 0 and 255)
        mask_b_black = source[b].point(lambda i: i == 0 and 255)
        mask_all_black = asarray(mask_r_black) * asarray(mask_g_black) * asarray(mask_b_black)
        # счет убираемых пикселей
        mask_r_white = source[r].point(lambda i: i == 255 and 255)
        mask_g_white = source[g].point(lambda i: i == 255 and 255)
        mask_b_white = source[b].point(lambda i: i == 255 and 255)
        mask_all_white = asarray(mask_r_white) * asarray(mask_g_white) * asarray(mask_b_white)
        return count_nonzero(mask_all_black)-count_nonzero(mask_all_white)

    def save_mask(self):
            # сохранение слоя
            match select_photo_condition.get():
                case "выбрать":
                    if self.good_pixel is not None:
                        self.true_good_pixel = self.good_pixel + self.number_point()
                    else:
                        self.true_good_pixel = self.number_point()
                case "исключить":
                    if self.all_pixel is not None:
                        self.true_all_pixel = self.all_pixel - self.number_point()
                    else:
                        self.true_all_pixel = shape(self.image_clean.split()[0])[0]*shape(self.image_clean.split()[0])[0] - self.number_point()
                    # TODO: проверить работоспособность
            # расчет ОП
            if self.true_good_pixel is not None and self.true_all_pixel is not None:
                entry_calculation.delete(0, END)
                entry_calculation.insert(0, str(self.true_good_pixel / self.true_all_pixel))

class Paint:
    def __init__(self):
        self.brush_size = 1
        self.color = 'black'

    # выбор цвета кисти
    def condition(self,event=1):
        if select_paint_condition.get() == "добавить":
            self.color = 'black'
        else:
            self.color = 'white'
        self.out_canvas()

    # размер кисти
    def brush(self,event):
        self.brush_size = var_brush_size.get()
        self.out_canvas()

    # нанесение рисунка
    def paint(self,event):
        photo.draw.ellipse([event.x-self.brush_size, event.y-self.brush_size, event.x+self.brush_size,
                            event.y+self.brush_size], fill= self.color, outline= self.color)
        canvas2.create_oval(event.x-self.brush_size, event.y-self.brush_size, event.x+self.brush_size,
                            event.y+self.brush_size, fill= self.color, outline= self.color)

    # вывод предварительного размера кисти
    def out_canvas(self):
        # закрашивание предыдущего рисунка
        canvas4.delete("oval")
        # нанесение нового рисунка
        canvas4.create_oval(24-self.brush_size, 24-self.brush_size,
                            24+self.brush_size,24+self.brush_size,fill='black', outline='black', tags='oval')

def b3(event):
    photo.rgb = photo.image_clean_resize.getpixel((event.x, event.y))
    canvas3['bg'] = '#%02x%02x%02x' % photo.rgb
    photo.scale_change()


# окно настроек счета
def radiobutton_changed(event=1):
    match select_photo_condition.get():
        case "нейтральное":
            if photo.flag:
                photo.out_image_clean()
        case "выбрать":
            if photo.rgb_good_pixel is not None:
                canvas3['bg'] = '#%02x%02x%02x' % photo.rgb_good_pixel
                photo.rgb = photo.rgb_good_pixel
                scale3.set(photo.error_good_pixel)
                photo.out_image_not_clean()
            else:
                canvas3['bg'] = "#f0f0f0"
        case "исключить":
            if photo.rgb_all_pixel is not None:
                canvas3['bg'] = '#%02x%02x%02x' % photo.rgb_all_pixel
                photo.rgb = photo.rgb_all_pixel
                scale3.set(photo.error_all_pixel)
                photo.out_image_delete()
            else:
                canvas3['bg'] = "#f0f0f0"


def help_click():
    messagebox.showinfo("Тех. поддержка", "89119659493\n Александр")


photo = Photo()
paint = Paint()

root = Tk()  # Создание окна
root.title("Не оптическая плотность")
root.geometry("900x700")

frame_photo = Frame(root)
frame_photo.pack(fill=BOTH, expand=True)

frame_setting = Frame(root)
frame_setting.pack(fill=Y)

frame_setting_photo = Frame(root)
frame_setting_photo.pack(fill=Y)

frame_setting_calculate = Frame(root)
frame_setting_calculate.pack(fill=Y)


# окно с фото
canvas2 = Canvas(frame_photo, width=photo.size[0], height=photo.size[1])
canvas2.pack(fill=BOTH, expand=1)


# окно настроек выбора
btn_select = Button(frame_setting, text="Выбор фото", width=11, font='ariel 15 bold', command=photo.select)
btn_select.pack(side=LEFT)

btn_save = Button(frame_setting, text="Сохранение", width=10, font='ariel 15 bold', command=photo.save)
btn_save.pack(side=LEFT)

btn_exit = Button(frame_setting, text="Выход", width=6, font='ariel 15 bold', command=root.destroy)
btn_exit.pack(side=LEFT)

paint_condition = ["добавить", "удалить"]
select_paint_condition = StringVar(value=paint_condition[0])

for condition in paint_condition:
    btn_paint_condition = Radiobutton(frame_setting, font="ariel 15 bold", text=condition, value=condition,
                                      variable=select_paint_condition, command=paint.condition)
    btn_paint_condition.pack(side=LEFT)

# толщина кисти
brush_size = Label(frame_setting, text="Толщина:", font="ariel 15 bold")
brush_size.pack(side=LEFT)
var_brush_size = IntVar(value=1)
scale_brush_size = Scale(frame_setting, from_=1, to=20, variable=var_brush_size,
                     orient=HORIZONTAL, command=paint.brush)
scale_brush_size.pack(side=LEFT)

canvas4 = Canvas(frame_setting, width="40", height="40", relief=RIDGE, bd=2)
canvas4.pack(side=LEFT)

# окно настроек фото
# яркость
bright = Label(frame_setting_photo, text="Яркость:", font="ariel 15 bold")
bright.pack(side=LEFT)
var_bright = IntVar(value=0)
scale_bright = Scale(frame_setting_photo, from_=-10, to=10, variable=var_bright,
                     orient=HORIZONTAL, command=photo.filter)
scale_bright.pack(side=LEFT)

# Контрастность
contrast = Label(frame_setting_photo, text="Контраст:", font="ariel 15 bold")
contrast.pack(side=LEFT)
var_contrast = IntVar(value=0)
scale_contrast = Scale(frame_setting_photo, from_=-10, to=10, variable=var_contrast,
                       orient=HORIZONTAL, command=photo.filter)
scale_contrast.pack(side=LEFT)

# Резкость
sharpness = Label(frame_setting_photo, text="Резкость:", font="ariel 15 bold")
sharpness.pack(side=LEFT)
var_sharpness = IntVar(value=0)
scale_sharpness = Scale(frame_setting_photo, from_=-10, to=10, variable=var_sharpness,
                        orient=HORIZONTAL, command=photo.filter)
scale_sharpness.pack(side=LEFT)

# Цветовой баланс
color_balance = Label(frame_setting_photo, text="Цветовой баланс", font="ariel 15 bold")
color_balance.pack(side=LEFT)
var_color_balance = IntVar(value=0)
scale_color_balance = Scale(frame_setting_photo, from_=-10, to=10, variable=var_color_balance,
                            orient=HORIZONTAL, command=photo.filter)
scale_color_balance.pack(side=LEFT)

# Состояние фото
photo_condition = ["нейтральное", "выбрать", "исключить"]
select_photo_condition = StringVar(value=photo_condition[0])

for condition in photo_condition:
    btn_photo_condition = Radiobutton(frame_setting_calculate, font="ariel 15 bold", text=condition, value=condition,
                                      variable=select_photo_condition, command=radiobutton_changed)
    btn_photo_condition.pack(side=LEFT)

# Размер выборки
v1 = IntVar()
scale3 = Scale(frame_setting_calculate, from_=0, to=100, variable=v1, orient=HORIZONTAL, command=photo.scale_change)
scale3.pack(side=LEFT)

canvas3 = Canvas(frame_setting_calculate, width="40", height="40", relief=RIDGE, bd=2)
canvas3.pack(side=LEFT)

btn_save_mask = Button(frame_setting_calculate, text="Сохранение слоя", width=15,
                       font='ariel 15 bold', command=photo.save_mask)
btn_save_mask.pack(side=LEFT)

entry_calculation = Entry(frame_setting_calculate, width=9, font='ariel 15 bold')
entry_calculation.pack(side=LEFT)

main_menu = Menu()

file_menu = Menu(font=("Verdana", 11, "bold"), tearoff=0)
file_menu.add_command(label="Открыть", command=photo.select)
file_menu.add_command(label="Сохранить", command=photo.save)
file_menu.add_separator()
file_menu.add_command(label="Выход", command=root.destroy)

main_menu.add_cascade(label="File", menu=file_menu)
main_menu.add_cascade(label="Тех. поддержка", command=help_click)

root.config(menu=main_menu)

canvas2.bind('<B1-Motion>', paint.paint)
canvas2.bind('<Button-3>', b3)
root.bind("<Configure>", photo.resize)

root.mainloop()

# TODO: добавить возможность убирать элементы в слое
# TODO:Добавить расчет закрашивания одинаковый для каждого слоя
# Просто относительно слоя прибавлять или вычитать результат
# Переделать способ рисования на линию
# Добавить линии в массив и с помощью кнопки их удалять