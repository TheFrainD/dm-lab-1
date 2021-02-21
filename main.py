import tkinter as tk
import random
import pickle
import algorithms as al

# Initializing sets
A = set()
B = set()
C = set()
U = set()

def save_to_file(master, inp):
    msg_window = tk.Toplevel(master)
    msg_window.title("Повідомлення")

    f = open('result.txt', 'ab')
    pickle.dump(inp, f)
    f.close()

    lbl_msg = tk.Label(msg_window,
                       text="Збережено!",
                       font="Helvetica 12 bold")
    lbl_msg.pack()

def error(msg):
    # Create error window
    error_window = tk.Toplevel(root)
    error_window.title("Помилка!")

    # Print the error
    lbl_error = tk.Label(error_window,
                         text=msg,
                         font="Helvetica 12 bold",
                         fg="red")
    lbl_error.pack()

def info():
    # Calculate the variant
    G = 5
    N = 8
    M = "ІО"
    if M == "ІО": N += 2
    Z = (N + G % 60) % 30 + 1
    
    # Create info window
    info = tk.Toplevel(root)
    info.title("Відомості про студента")

    # Print info
    lbl_name = tk.Label(info, text="ПІБ: Зиков Дмитро Олексійович")
    lbl_group = tk.Label(info, text="Група: ІО-05")
    lbl_number = tk.Label(info, text="Номер у списку: 8")
    lbl_variant = tk.Label(info, text="Варіант: {}".format(str(Z)))

    lbl_name.pack(padx=30)
    lbl_group.pack()
    lbl_number.pack()
    lbl_variant.pack()

def obtain_default():
    global A, B, C, U
    
    CUA = al.union(C, A)
    CUnA = al.union(C, al.not_set(A, U))
    result = al.symmetric_difference(A, al.difference(B, al.crossing(CUA, CUnA)))

    obtain_default_window = tk.Toplevel(root)
    obtain_default_window.title("Обчислення заданого виразу")

    def obtain():
        lbl_obtain = tk.Label(obtain_default_window, 
                              text="Розв'язок",
                              font="Helvetica 12 bold")
        lbl_obtained_result = tk.Label(obtain_default_window,
                                       justify="left",
                                       text="1) ¬A = {}\n".format(al.not_set(A, U)) +
                                           "2) C∪A = {}\n".format(CUA) +
                                           "3) C∪¬A = {}\n".format(CUnA) +
                                           "4) (C∪A)∩(C∪¬A) = {}\n".format(al.crossing(CUA, CUnA)) +
                                           "5) B\\(C∪A)∩(C∪¬A) = {}\n".format(al.difference(B, al.crossing(CUA, CUnA))) +
                                           "6) A△(B\\(C∪A)∩(C∪¬A) = {}\n\n".format(result) +
                                           "Відповідь: {}".format(result),
                                       font="Helvetica 12",
                                       borderwidth=2,
                                       relief="groove")
        
        lbl_obtain.grid(row=3, column=0, columnspan=2, sticky="W")
        lbl_obtained_result.grid(row=4, column=0, columnspan=2, sticky="W")

        btn_save['state'] = tk.NORMAL

    def save():
        save_to_file(obtain_default_window, result)

    lbl_expression = tk.Label(obtain_default_window,
                              text="D = A△(B\\(C∪A)∩(C∪¬A) = {}".format(result),
                              font="Helvetica 12 bold")
    lbl_sets = tk.Label(obtain_default_window,
                        text="A = {}\nB = {}\nC = {}".format(A, B, C),
                        font="Helvetica 12",
                        justify="left")
    btn_obtain = tk.Button(obtain_default_window,
                           text="Розв'язати",
                           command=obtain)
    btn_save = tk.Button(obtain_default_window,
                           text="Зберегти в файл",
                           state=tk.DISABLED,
                           command=save)

    lbl_expression.grid(row=0, column=0, columnspan=2, pady=10)
    lbl_sets.grid(row=1, column=0, columnspan=2, sticky="W")
    btn_obtain.grid(row=2, column=0, pady=10)
    btn_save.grid(row=2, column=1, pady=10)

# Enable "manual" entries and disable "random"
def radio_select_manual():
    ent_manualA['state'] = tk.NORMAL
    ent_manualB['state'] = tk.NORMAL
    ent_manualC['state'] = tk.NORMAL
    ent_cardinalityA['state'] = tk.DISABLED
    ent_cardinalityB['state'] = tk.DISABLED
    ent_cardinalityC['state'] = tk.DISABLED

# Enable "random" entries and disable "manual"
def radio_select_random():
    ent_manualA['state'] = tk.DISABLED
    ent_manualB['state'] = tk.DISABLED
    ent_manualC['state'] = tk.DISABLED
    ent_cardinalityA['state'] = tk.NORMAL
    ent_cardinalityB['state'] = tk.NORMAL
    ent_cardinalityC['state'] = tk.NORMAL

def are_entries_valid():
    inputs = [ent_uA.get(), ent_uB.get()]
    if choice.get() == 1:
        inputs.extend([ent_cardinalityA.get(), ent_cardinalityB.get(), ent_cardinalityC.get()])
    else:
        inputs.extend(ent_manualA.get().split(", "))
        inputs.extend(ent_manualB.get().split(", "))   
        inputs.extend(ent_manualC.get().split(", "))         

    for inp in inputs:
        if len(inp) == 0:
            error("Введення відсутнє!")
            return False
        elif not inp.isnumeric():
            error("Введення має бути в числовому форматі!")
            return False
        elif int(inp) not in range(0, 256):
            error("Числа мають бути в діапазоні від 0 до 255!")
            return False

    return True

def generate_random(start, stop, length):
    result = set()
    if length == 0: result.add(0)
    while len(result) < length:
        result.add(random.randint(start, stop))

    return result

def generate_manual(str):
    return set(list(map(int, str.split(", "))))

def generate_sets():
    if not are_entries_valid(): return False
    
    global A, B, C, U

    start = int(ent_uA.get())
    stop = int(ent_uB.get())

    var = choice.get()
    if var == 0:
        A = generate_manual(ent_manualA.get())
        B = generate_manual(ent_manualB.get())
        C = generate_manual(ent_manualC.get())
    else:
        A = generate_random(start, stop, int(ent_cardinalityA.get()))
        B = generate_random(start, stop, int(ent_cardinalityB.get()))
        C = generate_random(start, stop, int(ent_cardinalityC.get()))

    U = set(range(start, stop + 1))    

    # Output result
    lbl_result['text'] = "A = {}\nB = {}\nC = {}\nU = {}\n".format(A, B, C, U)

    # Give access to result windows
    btn_obtain_default['state'] = tk.NORMAL 
    btn_obtain_simplified['state'] = tk.NORMAL
    btn_symmetric_difference['state'] = tk.NORMAL
    btn_result['state'] = tk.NORMAL
        
# Create main window
root = tk.Tk()
root.title("Лабораторна робота №1")

btn_info = tk.Button(root,
                    text="Відомості про студента",
                    command=info)

# Radiobuttons choice
choice = tk.IntVar()
rbtn_manual = tk.Radiobutton(root, 
                            text="Ввести множину вручну",
                            variable=choice,
                            value=0,
                            command=radio_select_manual)
rbtn_random = tk.Radiobutton(root,
                            text="Згенерувати множину випадковим чином",
                            variable=choice,
                            value=1,
                            command=radio_select_random)

# Set manual creation
lbl_manual = tk.Label(root, text="Введіть множини")
lbl_manualA = tk.Label(root, text="A:")
lbl_manualB = tk.Label(root, text="B:")
lbl_manualC = tk.Label(root, text="C:")
ent_manualA = tk.Entry(root)
ent_manualB = tk.Entry(root)
ent_manualC = tk.Entry(root)

# Set random creation
lbl_random = tk.Label(root, text="Введіть потужність множин")
lbl_cardinalityA = tk.Label(root, text="A:")
lbl_cardinalityB = tk.Label(root, text="B:")
lbl_cardinalityC = tk.Label(root, text="C:")
ent_cardinalityA = tk.Entry(root)
ent_cardinalityB = tk.Entry(root)
ent_cardinalityC = tk.Entry(root)

# Default choice
radio_select_manual()

# Universal set parameters
lbl_universal = tk.Label(root, text="Задати універсальну множину")
lbl_uA = tk.Label(root, text="Від")
lbl_uB = tk.Label(root, text="До")
ent_uA = tk.Entry(root)
ent_uB = tk.Entry(root)

# Generate sets
btn_generate = tk.Button(root,
                        text="Згенерувати множини",
                        command=generate_sets)
lbl_result = tk.Label(root,
                    text = "A =\nB =\nC =\nU = \n",
                    justify = "left")

# Windows menu
btn_obtain_default = tk.Button(root,
                               text="Обчислення заданого виразу",
                               command=obtain_default,
                               state=tk.DISABLED)
btn_obtain_simplified = tk.Button(root,
                                  text="Обчислення спрощенного виразу",
                                  command=obtain_default,
                                  state=tk.DISABLED)
btn_symmetric_difference = tk.Button(root,
                                text="Симетрична різниця",
                                command=obtain_default,
                                state=tk.DISABLED)
btn_result = tk.Button(root,
                       text="Результати",
                       command=obtain_default,
                       state=tk.DISABLED)
# Place everything
btn_info.grid(row=0, column=1)
rbtn_manual.grid(row=1, column=1)
rbtn_random.grid(row=1, column=2)
lbl_manual.grid(row=2, column=1, sticky="W", padx=10)
lbl_manualA.grid(row=3, column=0, sticky="E")
lbl_manualB.grid(row=4, column=0, sticky="E")
lbl_manualC.grid(row=5, column=0, sticky="E")
ent_manualA.grid(row=3, column=1, sticky="W", padx=10)
ent_manualB.grid(row=4, column=1, sticky="W", padx=10)
ent_manualC.grid(row=5, column=1, sticky="W", padx=10)
lbl_random.grid(row=2, column=2, sticky="W", padx=10)
lbl_cardinalityA.grid(row=3, column=1, sticky="E")
lbl_cardinalityB.grid(row=4, column=1, sticky="E")
lbl_cardinalityC.grid(row=5, column=1, sticky="E")
ent_cardinalityA.grid(row=3, column=2, sticky="W", padx=10)
ent_cardinalityB.grid(row=4, column=2, sticky="W", padx=10)
ent_cardinalityC.grid(row=5, column=2, sticky="W", padx=10)
lbl_universal.grid(row=2, column=3, sticky="W", padx=10)
lbl_uA.grid(row=3, column=2, sticky="E")
lbl_uB.grid(row=4, column=2, sticky="E")
ent_uA.grid(row=3, column=3, sticky="W", padx=10)
ent_uB.grid(row=4, column=3, sticky="W", padx=10)
btn_generate.grid(row=0, column=3)
btn_obtain_default.grid(row=6, column=2, sticky="W")
btn_obtain_simplified.grid(row=6, column=3, sticky="W")
btn_symmetric_difference.grid(row=6, column=1, pady=10, sticky="W")
btn_result.grid(row=7, column=2, ipadx=50, pady=10, sticky="W")
lbl_result.grid(row=8, column=1, columnspan=3, sticky="W")

root.mainloop()