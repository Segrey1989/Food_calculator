from tkinter import *
from datetime import datetime

# проверка значения виджета Entry
def checkDigit(val):
    if not val.isalpha() and len(val) > 0:
        return True
    return False

# сортировка имеющихся данных при добавлении нового продукта
def sort():
    data = open('date.txt', 'r')
    arr = []
    for line in data:
        if len(line) > 1:
             arr.append(line)
    arr.sort()
    data.close()

    sortedData= open('date.txt', 'w')
    for line in arr:
        sortedData.write(line)
    sortedData.close()


# исключение повторения одной и той же даты в файле статистика
# все показатели за текущий день суммируются и записываются в итоге единожды
def calc_statistic():
    prot = 0
    fat = 0
    carb = 0
    energy = 0
    now = datetime.now()
    date = str(now.day) + "." + str(now.month) + "." + str(now.year)

    bufer = open('bufer.txt', 'w')
    statistic = open('Statistic.txt', 'r+')
    for line in statistic:
        arr = line.split(':')
        if arr[0] != date:
            bufer.write(line)

        if arr[0] == date:
            arr_items = arr[1].strip().split(" ")
            prot += float(arr_items[0])
            fat += float(arr_items[1])
            carb += float(arr_items[2])
            energy += float(arr_items[3])
    line = (str(date) + ": " + str(round(prot,1)) + " " + str(round(fat,1)) + " " + str(round(carb,1)) + " " + str(round(energy,1)) + "\n")
    bufer.write(line)
    bufer.close()
    statistic.close()

    statistic = open('Statistic.txt', 'w')
    bufer = open('bufer.txt', 'r')
    for line in bufer:
        statistic.write(line)

    bufer.close()
    statistic.close()

# Отоброжение каждого показателя в сумме за день
def get_day_values(day_arr):
    f = open('dayStat.txt', 'r')
    line = f.read()
    arr = line.split(' ')
    day_arr[0]['text'] = arr[0]
    day_arr[1]['text'] = arr[1]
    day_arr[2]['text'] = arr[2]
    day_arr[3]['text']= arr[3]
    f.close()

# Отображение показателей последнего продукта
def get_item_value(item_arr, prot, fat, carb, energy):
    item_arr[0]['text'] =  prot
    item_arr[1]['text'] =   fat
    item_arr[2]['text'] =  carb
    item_arr[3]['text'] =  energy

# Изменение дневных значений при внесении нового продукта
def change_day_values(prot, fat, carb, energy):
    f = open('dayStat.txt', 'r')
    line = f.read()
    arr = line.split(' ')
    f.close()

    arr[0]= round(float(arr[0]) + prot, 1)
    arr[1] = round(float(arr[1])+ fat, 1)
    arr[2] = round(float(arr[2])+ carb,1)
    arr[3] = round(float(arr[3])+ energy,1)

    f = open('dayStat.txt', 'w')
    for i in arr:
        f.write(str(i) + ' ')
    f.close()


# Обнуление счетчиков и занесение данных в историю
def new_day_values(lab, but, ent1, ent2, arr):
    now = datetime.now()

    f = open('dayStat.txt', 'r')
    line = f.read()
    f.close()

    f = open('dayStat.txt', 'w')
    f.write('0 0 0 0')
    f.close()

    statistic =open('Statistic.txt', 'a')
    date = str(now.day) + "." + str(now.month) + "." + str(now.year) + ":\t" + line + "\n"

    statistic.write(date)
    statistic.close()

    get_day_values(day_arr)
    but['text'] = "Добавить"
    lab['text'] = "Название продукта"
    ent1.delete(0, END)
    ent2.delete(0, END)
    for item in arr:
        item['text'] = 0

    calc_statistic()
    fra3.grid_remove()
    lab['fg'] = 'SteelBlue'
    but['command'] = lambda: callback(lab2, but, entry_arr)
    for item in add_ent_arr:
        item.delete(0, END)
    ent.focus_set()

# функция поиска продукта в списке и подсчет показателей
def callback(lab2, but, entry_arr):
    weight = entry_arr[1].get()
    f = open('date.txt', 'r')
    f.seek(0)

    for line in f:
       arr = line.lower().split(' ')
       str_line = ''
       for i in range(0, len(arr)-4):
           str_line += arr[i] + " "
       if not checkDigit(weight) or len(entry_arr[0].get().strip()) < 1:
           ent_weight.delete(0, END)
           return
       if str_line.strip() == ent.get().strip().lower() :
            dayProt = round(float(arr[-4])/100 * float(weight),1)
            dayFat = round(float(arr[-3])/100 * float(weight),1)
            dayCarb = round(float(arr[-2])/100 * float(weight),1)
            dayEnergy = round(float(arr[-1])/100 * float(weight),1)
            get_item_value(item_arr, dayProt, dayFat, dayCarb, dayEnergy)
            change_day_values(dayProt, dayFat, dayCarb, dayEnergy)
            get_day_values(day_arr)

            for item in entry_arr:
                item.delete(0, END)
            entry_arr[0].focus_set()
            f.close()
            return
    f.close()
    lab2['text'] = "Нет в списке"
    but['text'] = 'Внести'
    root.maxsize(400, 350)
    root.minsize(400, 350)
    fra3.grid( padx =30, pady = 5, sticky= 'nw')
    add_ent_arr[0].focus_set()
    cur_weight_val = entry_arr[1].get()
    entry_arr[1].delete(0, END)
    entry_arr[1].insert(0, '100')
    if but['text'] == 'Внести':
        but['command'] = lambda: append(but, lab2, entry_arr, add_ent_arr, cur_weight_val)


# Добавление продукта в список при его отсутствии в нем
def append(but, lab, entry_arr, add_ent_arr, cur_weight_val):
    flag = False
    add_ent_val = []
    for item in add_ent_arr:
        val = item.get().strip()
        # if not val.isalpha() and len(val) > 0:
        if checkDigit(val):
            add_ent_val.append(str(round(float(val),1)))
        else:
            item.delete(0, END)
            add_ent_val = []

    f = open('date.txt', 'a+')
    f.seek(2)
    f.write("\n")

    if len(add_ent_val) == 4:
        text= (ent.get().strip().lower() + " " + add_ent_val[0] + " " + add_ent_val[1] + " " +add_ent_val[2] + " " +add_ent_val[3] + '\n' )
        f.write(text)
        f.close()
        sort()
        for item in add_ent_arr:
            item.delete(0, END)
            root.maxsize(400, 270)
            root.minsize(400, 270)
        entry_arr[1].delete(0, END)
        entry_arr[1].insert(0, cur_weight_val)


        but['text'] = 'Добавить'
        lab['text'] = "Название продукта: "
        lab['fg'] = 'SteelBlue'
        flag = True

    else:
        lab['text'] = "Некорректные данные!"
        lab['fg'] = 'red'


    if flag == True:
        fra3.grid_remove()
        but['command'] = lambda:callback(lab2, but,  entry_arr)


# вспомогательная: очистка значений lab
def clean_items_val(arr):
    for item in arr:
        item['text'] = 0

# отменить добавление последнего введенного продукта
def del_last_product(item_arr):
    f = open('dayStat.txt', 'r')
    line = f.read()
    arr = line.split(' ')
    f.close()

    for i in range(0, 4):
        arr[i] = round(float(arr[i]) - item_arr[i].cget('text'), 1)
        arr[i] = str(arr[i])

    f = open('dayStat.txt', 'w')
    f.write(' '.join(arr))
    f.close()
    get_day_values(day_arr)
    clean_items_val(item_arr)



# сбросить и спрятать поля fra3 при нажатии на кнопку
def cancel_adding(arr, but, lab2, entry_arr):
    for item in arr:
        item.delete(0, END)
    fra3.grid_remove()
    but['command'] = lambda: callback(lab2, but, entry_arr)
    but['text'] = 'Добавить'
    lab2['text'] = "Название продукта: "
    lab2['fg'] = 'SteelBlue'
    entry_arr[0].delete(0, END)
    entry_arr[1].delete(0, END)
    root.maxsize(400, 270)
    root.minsize(400, 270)
    ent.focus_set()



root = Tk()
root.maxsize(400,270)
root.minsize(400,270)

# Рамки
fra1 = Frame(root, highlightcolor = 'red')
fra2 = Frame(root, bd = 2)
fra3 = Frame(root, bd = 0)

# Labels
now = datetime.now()
str_line2 = str(now.day) + '.' + str(now.month)+ '.' + str(now.year)[-2:]
lab1 = Label(fra1,
             text =  str_line2,
             justify = 'left',
             font = 'Impact 17 bold',
             fg = 'SteelBlue',
             bd = 2,
             activeforeground = 'Red')

lab_day = Label(fra1,
          text = "День: ",
          font = 'Herald 12',
          fg = 'Black',)

lab_item = Label(fra1,
          text = "Последний продукт: ",
          font = 'Herald 12',
          fg = 'Black')

protLab = Label(fra1,
          text = "Белки: ",
          font = 'Courier 15 bold',
          fg = 'Black')

fatLab = Label(fra1,
          text = "Жиры: ",
          font = 'Courier 15 bold',
          fg = 'Black')

carbLab = Label(fra1,
           text = "Углеводы: ",
           font = 'Courier 15 bold',
           fg = 'Black')

energyLab = Label(fra1,
             text = "Ккал: ",
             font = 'Courier 15 bold',
             fg = 'Black')

protVal = Label(fra1)
fatVal = Label(fra1)
carbVal = Label(fra1)
energyVal = Label(fra1)

item_energy_val = Label(fra1)
item_carb_val = Label(fra1)
item_fat_val = Label(fra1)
item_prot_val = Label(fra1)


lab2 = Label(fra2,
             text = 'Название продукта: ',
             justify='left',
             font='Geneva 15 bold',
             fg='SteelBlue',
             bd=2,
             )

lab3 = Label(fra2,
             text = 'Грамм: ',
             justify='left',
             font='Geneva 15 bold',
             fg='SteelBlue',
             bd=2,
             )

add_prot = Label(fra3,
                 text='Белки:',
                 justify='left',
                 font='Courier 14',
                 fg='LightSteelBlue',
                 bd=2,
                 )

add_fat = Label(fra3,
                 text='Жиры:',
                 justify='left',
                 font='Courier 14',
                 fg='LightSteelBlue',
                 bd=2,
                 )

add_carb = Label(fra3,
                 text='Углеводы:',
                 justify='left',
                 font='Courier 14',
                 fg='LightSteelBlue',
                 bd=2,
                 )

add_energy = Label(fra3,
                 text='Ккал:',
                 justify='left',
                 font='Courier 14',
                 fg='LightSteelBlue',
                 bd=2,
                 )

# Buttons
newDay = Button(fra1,
             text = "Обнулить",
             font='Geneva 13',
             width = 10,
             highlightbackground='lightsteelblue',
             command = lambda: new_day_values(lab2, but, ent,ent_weight, item_arr)
                )

but = Button(fra2,
             text = "Добавить",
             font='Geneva 13',
             width = 10,
             foreground = 'red',
             highlightbackground='lightsteelblue',
             command=lambda:callback(lab2, but, entry_arr)
             )

del_last_but = Button(fra1, width=8,
                      highlightbackground='tomato',
                       text = 'Назад',
                      font = 'Geneva 13',
                      command = lambda: del_last_product(item_arr)
                      )

cancel_adding_but = Button(fra3, width=40,
                      highlightbackground='tomato',
                       text = 'Отменить',
                      font = 'Geneva 13',
                      command = lambda: cancel_adding(add_ent_arr, but, lab2, entry_arr)
                      )


ent = Entry(fra2)
ent_weight = Entry(fra2,  width = 5)

add_prot_ent = Entry(fra3,  width=7)
add_fat_ent = Entry(fra3, width=7)
add_carb_ent = Entry(fra3, width=7)
add_energy_ent = Entry(fra3,  width=7)

# Arrays of values
item_arr = [item_prot_val, item_fat_val, item_carb_val, item_energy_val]
day_arr = [protVal, fatVal, carbVal, energyVal]
entry_arr = [ent, ent_weight]
add_ent_arr = [add_prot_ent, add_fat_ent, add_carb_ent, add_energy_ent]

# Фокус на поле ввода при запуске программы
# отображение значений за день при запуске
ent.focus_set()
get_day_values(day_arr)

# обнуление значений последнего продукта
clean_items_val(item_arr)

fra1.grid(ipadx =40,
             ipady=10,
              padx =30,
             pady=5,
          sticky= 'nw')
fra2.grid( padx =10, sticky= 'nw')

# fra1
lab1.grid(row=0, column=0, columnspan = 2, padx= 20, sticky=(N,W))
protLab.grid(row=2, column=0)
fatLab.grid(row=3, column=0)
carbLab.grid(row=4, column=0)
energyLab.grid(row=5, column=0)

newDay.grid(row= 0, column=2)

lab_day.grid(row=1, column=1)
lab_item .grid(row=1, column=2)

protVal.grid(row=2, column=1)
item_prot_val.grid(row=2, column=2)

fatVal.grid(row=3, column=1)
item_fat_val.grid(row=3, column=2)

carbVal.grid(row=4, column=1)
item_carb_val.grid(row=4, column=2)

energyVal.grid(row=5, column=1)
item_energy_val.grid(row=5, column=2)

del_last_but.grid(row=5, column=3)

ent.grid(row=1, column=0,  sticky=(N,W))
ent_weight.grid(row=1, column=1)


# fra2
lab2.grid(row=0, column=0,   sticky=(N,W))
lab3.grid(row=0, column=1, sticky=(N,W))
but.grid(row= 1, column=2)

# Поля для добавления нутриентов
# fra3
add_prot.grid(row=0, column = 0)
add_prot_ent.grid(row=1, column = 0)

add_fat.grid(row=0, column = 1)
add_fat_ent.grid(row=1, column = 1)

add_carb.grid(row=0, column = 2)
add_carb_ent.grid(row=1, column = 2)

add_energy.grid(row=0, column = 3)
add_energy_ent.grid(row=1, column = 3)

cancel_adding_but.grid(row=3, column=0, columnspan=4, pady = 10)
root.mainloop()