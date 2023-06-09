import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
from tkcalendar import DateEntry
from time import strftime
from functools import partial
from collections import deque

# Subfiles
import database as db

# Queue


def enqueue(queue, value):
    queue.append(value)


def dequeue(queue):
    queue.popleft()


def front(queue):
    return queue[0]


def empty_queue(queue):
    return len(queue) == 0


def transform_str(string):
    return string.replace(",", ".")

def transform_dot(string):
    return string.replace(".", "")
# Frontend


class Abstract:
    def __init__(self, name):
        # Initializing of GUI
        self.workspace = tk.Tk()
        self.workspace.title(name)
        self.workspace.resizable(width=False, height=False)
        self.workspace.configure(bg="gray2")
        self.workspace.columnconfigure(8, weight=1)
        self.width = 1200
        self.height = 900
        self.sc_width = self.workspace.winfo_screenwidth()
        self.sc_height = self.workspace.winfo_screenheight()
        self.x = (self.sc_width / 2) - (self.width / 2)
        self.y = (self.sc_height / 3) - (self.height / 3)
        self.workspace.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y))


class MainWorkspace(Abstract):
    def __init__(self, name):
        super().__init__(name)
        self.vending_machine = None
        self.logo = tk.PhotoImage(file="machine_logo.png")
        # Date and time
        self.time = strftime("%H:%M:%S")
        self.date = strftime('%d-%B-%Y')
        self.selling_date = strftime('%Y-%m-%d')
        # Frames
        # header
        self.main_color = "green2"
        self.header = tk.Frame(self.workspace, width=self.width - 28, height=self.height / 8, bg="gray12")
        self.header.grid(row=0, column=0, pady=2, padx=2, ipady=2, ipadx=2, sticky="NW")
        self.header.columnconfigure(4, weight=1)
        self.title_label = tk.Label(self.header, text="VENDING MACHINE", font="Arial 20 bold", bg="gray12", fg=self.main_color)
        self.title_label.grid(row=0, column=0, columnspan=3, ipadx=460, padx=4, ipady=20, sticky="NSWE")
        self.store_button = tk.Button(self.header, text="Sklad", command=self.open_warehouse, font="Arial 15 bold", bg="gray26", fg="green3")
        self.store_button.grid(row=1, column=1, sticky="EW", ipadx=200)
        self.time_label = tk.Label(self.header, text=self.time, font=("Arial", 17), bg="gray12", fg=self.main_color)
        self.time_label.grid(row=1, column=0, ipadx=40, padx=4, ipady=15, sticky="W")
        self.date_label = tk.Label(self.header, text=self.date, font=("Arial", 17), bg="gray12", fg=self.main_color)
        self.date_label.grid(row=1, column=2, ipadx=40, padx=4, ipady=15, sticky="E")
        # vending area
        self.vending_area = tk.Frame(self.workspace, width=1000, height=748, bg="gray22")
        self.vending_area.grid(row=1, column=0, pady=2, padx=2, sticky="NSWE")
        self.vending_area.grid_propagate(False)
        self.vending_area.columnconfigure(5, weight=1)
        self.vending_area.rowconfigure(6, weight=1)

        # Buttons
        self.hor_mover = 0
        self.ver_mover = 0
        self.plus = tk.Button(self.vending_area, text="+", command=self.add_machine, font="Arial 20", bg="gray26", fg="white")
        self.plus.grid(row=self.ver_mover, column=self.hor_mover, pady=40, ipady=4, padx=40, ipadx=4, rowspan=2)

        # Inside functions
        self.time_refresh()

        # Vending machines - container
        self.new_name = None
        self.machine_label = None
        self.machine_container = []

        # Load containers
    def unpacking_dat(self):
        with open("machine_container.txt", "r") as dat_machines:
            for machine in dat_machines.read().split("**"):
                if machine == "":
                    pass
                else:
                    self.machine_container.append(machine)
            return self.machine_container

    def packing_dat(self):
        with open("machine_container.txt", "w") as dat_machines:
            for machine in self.machine_container:
                machine = machine + "**"
                dat_machines.write(machine)

        # Vending machines

    def add_machine(self):
        self.new_name = simpledialog.askstring("Nový automat", "Zadaj názov automatu: ")
        self.new_name = transform_dot(self.new_name)
        if self.new_name:
            self.plus.destroy()
            self.machine_label = tk.Label(self.vending_area, text=self.new_name, font="Aerial 14 bold", bg="gray22", fg="white")
            self.machine_label.grid(row=self.ver_mover, column=self.hor_mover, padx=2, pady=20)
            self.vending_machine = tk.Button(self.vending_area, image=self.logo, command=partial(self.open_machine, self.new_name))
            self.vending_machine.grid(row=self.ver_mover+1, column=self.hor_mover, padx=90)
            self.machine_container.append(self.machine_label.cget("text"))
            db.create_table(self.new_name, "tovar VARCHAR(20), cena_s_dph FLOAT(4), predajna_cena FLOAT(4), pocet_kusov INT", "tovar, cena_s_dph")
            db.create_table(self.new_name + "_predaje", "(datum DATE, tovar VARCHAR(20), cena_s_dph FLOAT(4), predajna_cena FLOAT(4), pocet_kusov INT, status VARCHAR(4))")
            self.packing_dat()
            self.hor_mover += 1
            if self.hor_mover == 4:
                self.hor_mover = 0
                self.ver_mover += 2
                self.plus = tk.Button(self.vending_area, text="+", command=self.add_machine, font="aerial 20", bg="gray26", fg="white")
                self.plus.grid(row=self.ver_mover, column=self.hor_mover, pady=40, ipady=4, padx=40, ipadx=4, rowspan=2)
            elif self.hor_mover == 4 and self.ver_mover == 4:
                self.plus.destroy()
            else:
                self.plus = tk.Button(self.vending_area, text="+", command=self.add_machine, font="aerial 20", bg="gray26", fg="white")
                self.plus.grid(row=self.ver_mover, column=self.hor_mover, pady=40, ipady=4, padx=40, ipadx=4, rowspan=2)
        return self.machine_container

    def date_refresh(self):
        self.date = strftime('%d-%B-%Y')
        self.date_label.config(text=self.date)
        self.date_label.after(1000, self.date_refresh)

    def time_refresh(self):
        self.time = strftime("%H:%M:%S")
        self.time_label.config(text=self.time)
        self.time_label.after(1000, self.time_refresh)
        if self.time >= strftime("00:00:00"):
            self.date_refresh()

    def initiate_base_state(self):
        if len(self.machine_container) != 0:
            for machine in self.machine_container:
                self.plus.destroy()
                machine = machine
                self.machine_label = tk.Label(self.vending_area, text=machine, font="Aerial 14 bold", bg="gray22", fg="white")
                self.machine_label.grid(row=self.ver_mover, column=self.hor_mover, padx=2, pady=20)
                self.vending_machine = tk.Button(self.vending_area, image=self.logo, command=partial(self.open_machine, machine))
                self.vending_machine.grid(row=self.ver_mover + 1, column=self.hor_mover, padx=90)
                self.hor_mover += 1
                if self.hor_mover == 4:
                    self.hor_mover = 0
                    self.ver_mover += 2
                    self.plus = tk.Button(self.vending_area, text="+", command=self.add_machine, font="aerial 20", bg="gray26", fg="white")
                    self.plus.grid(row=self.ver_mover, column=self.hor_mover, pady=40, ipady=4, padx=40, ipadx=4, rowspan=2)
                elif self.hor_mover == 4 and self.ver_mover == 4:
                    self.plus.destroy()
                else:
                    self.plus = tk.Button(self.vending_area, text="+", command=self.add_machine, font="aerial 20", bg="gray26", fg="white")
                    self.plus.grid(row=self.ver_mover, column=self.hor_mover, pady=40, ipady=4, padx=40, ipadx=4, rowspan=2)

    def open_warehouse(self):
        self.workspace.withdraw()
        wh = Warehouse('Warehouse')
        wh.workspace.protocol("WM_DELETE_WINDOW", wh.close_warehouse)
        wh.refresh_state()
        wh.run_wh()

    @staticmethod
    def open_machine(machine_name):
        machine_name = VendingMachine(machine_name)
        machine_name.refresh_machine_state()
        machine_name.run_machine()

    def run(self):
        self.workspace.mainloop()


class Warehouse(Abstract):
    def __init__(self, name):
        super().__init__(name)
        self.workspace.configure(bg="gray22")
        self.workspace.geometry("990x900")
        self.width = 990
        self.height = 900
        self.wh_workspace = tk.Frame(self.workspace, bg="gray26", height=self.height, width=self.width)
        self.wh_workspace.grid(row=0, column=0, sticky="NSWE")
        self.wh_workspace.rowconfigure(10, weight=1)
        self.wh_workspace.columnconfigure(8, weight=1)
        self.wh_table = ttk.Treeview(self.wh_workspace, show="headings", columns=('c1', 'c2', 'c3'), height=43)
        self.wh_table.grid(row=0, column=0, columnspan=3, rowspan=20, pady=10, padx=10, sticky="NW")

        self.wh_table.column('c1', anchor="center", width=200)
        self.wh_table.heading('c1', text="Tovar:")
        self.wh_table.column('c2', anchor="center", width=200)
        self.wh_table.heading('c2', text="Cena s DPH:")
        self.wh_table.column('c3', anchor="center", width=200)
        self.wh_table.heading('c3', text="Počet kusov:",)
        self.wh_worth = 0

        # Buttons
        self.wh_state_label = tk.Label(self.wh_workspace, text="Hodnota skladu: ", font="Arial 15 bold", bg="gray26", fg="white")
        self.wh_state_label.grid(row=0, column=4, padx=10, pady=20, ipadx=20, sticky="N")
        self.wh_state = tk.Label(self.wh_workspace, text=self.wh_worth, font="Arial 15 bold", bg="gray26", fg="white")
        self.wh_state.grid(row=0, column=5, padx=10, pady=20, ipadx=20, sticky="N")
        self.add_button = tk.Button(self.wh_workspace, text='Nový nákup', command=self.add_goods, font="Arial 12 bold", bg="gray26", fg="white")
        self.add_button.grid(row=1, column=4, columnspan=2, padx=10, pady=4, ipadx=100, sticky="NEW")
        self.add_button = tk.Button(self.wh_workspace, text='Znížiť stav', command=self.remove_goods, font="Arial 12 bold", bg="gray26", fg="white")
        self.add_button.grid(row=2, column=4, columnspan=2, padx=10, pady=4, ipadx=100, sticky="NEW")

        # Autoload
        self.new_purchase = None
        self.purchase_date_label = None
        self.purchase_date = None
        self.good_label = None
        self.price_label = None
        self.refundable_label = None
        self.amount_label = None
        self.price_w_ref = 0

        self.wh_items = set()
        self.wh_stocks = []
        self.good_name_cont = []
        self.purchase_cont = []
        self.refundable_vars = []
        self.name_of_good = None
        self.price_entry = None
        self.refundable_check = None
        self.price_lab = None
        self.amount_lab = None
        self.for_reducing = None
        self.reduced = None
        self.amount_entry = None
        self.ref_var = tk.IntVar(self.new_purchase, value=0)
        self.row_counter = 0
        self.plus_row = None
        self.temp = 0
        self.new_good = None

    def calculate_wh(self):
        self.wh_worth = db.make_sum('cena_s_dph * pocet_kusov', 'vending_db.sklad')[0][0]
        if self.wh_worth is None:
            self.wh_state.config(text=str(0) + " €")
        else:
            self.wh_state.config(text=str(round(self.wh_worth, 2)) + " €")

    def refresh_state(self):
        self.calculate_wh()
        for y in self.wh_table.get_children():
            self.wh_table.delete(y)
        self.wh_stocks = db.refresh_db("*", "vending_db.sklad")
        for x in self.wh_stocks:
            item, price, amount = x
            self.wh_table.insert('', 'end', values=(str(item), str(price), str(amount)))
            self.wh_items.add(str(x[0]))

    def clean_and_load(self):
        self.good_name_cont = []
        self.purchase_cont = []

    def make_purchase(self):
        for idx, item in enumerate(self.good_name_cont):
            price, amount, var = self.purchase_cont[idx]
            price = transform_str(price.get())
            amount = transform_str(amount.get())
            var = var.get()
            if len(price) == 0 or len(amount) == 0:
                print("Nothing happend")
            elif var == 0:
                db.insert_db("vending_db.sklad", "(tovar, cena_s_dph, pocet_kusov)", str((item, float(price), amount)), "pocet_kusov = pocet_kusov + " + str(amount))
                db.insert_db("vending_db.nakupy", "(datum, tovar, nakupna_cena, pocet_kusov)", str((self.purchase_date.get(), item, float(price), amount)))
            elif var == 1:
                self.price_w_ref = float(price) + 0.15
                db.insert_db("vending_db.sklad", "(tovar, cena_s_dph, pocet_kusov)", str((item, float(self.price_w_ref), amount)), "pocet_kusov = pocet_kusov + " + str(amount))
                db.insert_db("vending_db.nakupy", "(datum, tovar, nakupna_cena, pocet_kusov)", str((self.purchase_date.get(), item, float(self.price_w_ref), amount)))
        self.close_toplevel()

    def add_goods(self):
        self.new_purchase = tk.Toplevel(self.wh_workspace, bg="gray22")
        self.new_purchase.geometry("800x1000")
        self.new_purchase.protocol("WM_DELETE_WINDOW", self.close_toplevel)
        self.purchase_date_label = tk.Label(self.new_purchase, text="Dátum nákupu: ", font="Arial 12 bold", bg="gray26", fg="white")
        self.purchase_date_label.grid(row=0, column=4, padx=10, pady=6)
        self.purchase_date = DateEntry(self.new_purchase, date_pattern='yyyy-mm-dd')
        self.purchase_date.grid(row=0, column=5, padx=10, pady=4)
        self.good_label = tk.Label(self.new_purchase, text="Tovar", font="Arial 12", fg="white", bg="gray26")
        self.good_label.grid(row=0, column=0, padx=10, pady=4)
        self.price_label = tk.Label(self.new_purchase, text="Nák. cena s DPH", font="Arial 12", fg="white", bg="gray26")
        self.price_label.grid(row=0, column=1, padx=10, pady=4)
        self.amount_label = tk.Label(self.new_purchase, text="Množstvo", font="Arial 12", fg="white", bg="gray26")
        self.amount_label.grid(row=0, column=2, padx=10, pady=4)
        self.refundable_label = tk.Label(self.new_purchase, text="Zálohovanie", font="Arial 12", fg="white", bg="gray26")
        self.refundable_label.grid(row=0, column=3, padx=10, pady=4)
        tk.Button(self.new_purchase, text="Potvrdiť", command=self.make_purchase, font="Arial 12 bold", bg="gray26", fg="white").grid(row=1, column=4, columnspan=2, sticky="WE")
        self.wh_stocks = db.refresh_db("tovar", "vending_db.sklad")
        for idx, tovar in enumerate(set(self.wh_stocks)):
            tovar = tovar[0]
            self.name_of_good = tk.Label(self.new_purchase, text=tovar, anchor="w", font="Arial 10", bg="gray22", fg="white")
            self.name_of_good.grid(row=idx + 1, column=0, pady=2, padx=2)
            self.good_name_cont.append(self.name_of_good.cget('text'))
            self.price_entry = tk.Entry(self.new_purchase, width=10)
            self.price_entry.grid(row=idx + 1, column=1)
            self.amount_entry = tk.Entry(self.new_purchase, width=10)
            self.amount_entry.grid(row=idx + 1, column=2)
            self.ref_var = tk.IntVar(self.new_purchase, value=0)
            self.refundable_check = tk.Checkbutton(self.new_purchase, variable=self.ref_var, onvalue=1, offvalue=0, bg="gray26")
            self.refundable_check.grid(row=idx + 1, column=3)
            self.purchase_cont.append((self.price_entry, self.amount_entry, self.ref_var))
            self.row_counter = idx + 1
        self.plus_row = tk.Button(self.new_purchase, text="+", command=self.add_new_good, anchor="w", font="Arial 11", bg="gray22", fg="white")
        self.plus_row.grid(row=self.row_counter + 2, column=0, pady=4)

    def add_new_good(self):
        self.new_good = simpledialog.askstring("Nový tovar", "Zadaj názov tovaru: ")
        if self.new_good:
            self.plus_row.destroy()
            self.name_of_good = tk.Label(self.new_purchase, text=self.new_good, anchor="w", font="Arial 10", bg="gray22", fg="white")
            self.name_of_good.grid(row=self.row_counter + 1, column=0, pady=2, padx=2)
            self.good_name_cont.append(self.name_of_good.cget('text'))
            self.price_entry = tk.Entry(self.new_purchase, width=10)
            self.price_entry.grid(row=self.row_counter + 1, column=1)
            self.amount_entry = tk.Entry(self.new_purchase, width=10)
            self.amount_entry.grid(row=self.row_counter + 1, column=2)
            self.ref_var = tk.IntVar(self.new_purchase, value=0)
            self.refundable_check = tk.Checkbutton(self.new_purchase, variable=self.ref_var, onvalue=1, offvalue=0, bg="gray26")
            self.refundable_check.grid(row=self.row_counter + 1, column=3)
            self.purchase_cont.append((self.price_entry, self.amount_entry, self.ref_var))
            self.row_counter += 1
            self.plus_row = tk.Button(self.new_purchase, text="+", command=self.add_new_good, anchor="w", font="Arial 10", bg="gray22", fg="white")
            self.plus_row.grid(row=self.row_counter + 1, column=0, pady=4)

    def remove_wh_good(self):
        for x in self.purchase_cont:
            good, price, amount, change = x
            change = change.get()
            if len(change) == 0:
                pass
            else:
                db.insert_db("vending_db.sklad", "(tovar, cena_s_dph, pocet_kusov)", str((good, float(price), amount)), "pocet_kusov = pocet_kusov - " + str(change))
                db.insert_db("vending_db.nakupy", "(datum, tovar, nakupna_cena, pocet_kusov)", str((gui.selling_date, good, float(price), amount)))
            db.remove_from_db('vending_db.sklad', 'pocet_kusov = 0')
        self.close_toplevel()

    def remove_goods(self):
        self.new_purchase = tk.Toplevel(self.wh_workspace, bg="gray22")
        self.new_purchase.geometry("800x1000")
        self.new_purchase.protocol("WM_DELETE_WINDOW", self.close_toplevel)
        #self.scrollbar = tk.Scrollbar(self.new_purchase)
        #self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.purchase_date_label = tk.Label(self.new_purchase, text="Dátum nákupu: ", font="Arial 12 bold", bg="gray26", fg="white")
        self.purchase_date_label.grid(row=0, column=4, padx=10, pady=6)
        self.purchase_date = DateEntry(self.new_purchase, date_pattern='dd-mm-yyyy')
        self.purchase_date.grid(row=0, column=5, padx=10, pady=4)
        self.good_label = tk.Label(self.new_purchase, text="Tovar", font="Arial 12", fg="white", bg="gray26")
        self.good_label.grid(row=0, column=0, padx=10, pady=4)
        self.price_label = tk.Label(self.new_purchase, text="Nák. cena s DPH", font="Arial 12", fg="white", bg="gray26")
        self.price_label.grid(row=0, column=1, padx=10, pady=4)
        self.amount_label = tk.Label(self.new_purchase, text="Množstvo", font="Arial 12", fg="white", bg="gray26")
        self.amount_label.grid(row=0, column=2, padx=10, pady=4)
        self.reduced = tk.Label(self.new_purchase, text="Odpočítať", font="Arial 12", fg="white", bg="gray26")
        self.reduced.grid(row=0, column=3, padx=10, pady=4)
        tk.Button(self.new_purchase, text="Odpočítať", command=self.remove_wh_good, font="Arial 12 bold", bg="gray26", fg="white").grid(row=1, column=4, columnspan=2, sticky="WE")
        self.wh_stocks = db.refresh_db("*", "vending_db.sklad")
        for idx, x in enumerate(set(self.wh_stocks)):
            tovar, cena, mnozstvo = x
            self.name_of_good = tk.Label(self.new_purchase, text=tovar, anchor="w", font="Arial 10", bg="gray22", fg="white")
            self.name_of_good.grid(row=idx + 1, column=0, pady=2, padx=2)
            self.price_lab = tk.Label(self.new_purchase, text=cena, width=10)
            self.price_lab.grid(row=idx + 1, column=1)
            self.amount_lab = tk.Label(self.new_purchase, text=mnozstvo, width=10)
            self.amount_lab.grid(row=idx + 1, column=2)
            self.for_reducing = tk.Entry(self.new_purchase, width=10)
            self.for_reducing.grid(row=idx + 1, column=3)
            self.purchase_cont.append((tovar, self.price_lab.cget('text'), self.amount_lab.cget('text'), self.for_reducing))
            self.row_counter = idx + 1

    def close_toplevel(self):
        self.clean_and_load()
        self.new_purchase.destroy()
        self.refresh_state()

    def close_warehouse(self):
        self.workspace.destroy()
        gui.workspace.deiconify()

    def run_wh(self):
        self.workspace.mainloop()


class VendingMachine(Abstract):
    def __init__(self, name):
        super().__init__(name)
        self.machine = name
        # Autoload
        # refresh state
        self.machine_good = None
        self.warehouse_price = None
        self.machine_price = None
        self.machine_amount = None
        #self.name_of_goods = []
        self.machine_content = []
        self.machine_content2 = []
        self.wh_stocks = []
        self.wh = {}
        self.wh_stack = None
        self.machine_prices_container = []
        self.machine_worth = 0
        self.aux_wh = 0

        self.machine_prices_check = {}

        # Toplevel
        self.machine_top = None
        self.machine_date = None
        self.machine_date_lab = None
        self.machine_price_lab = None
        self.good_lab = None
        self.wh_price_lab = None
        self.confirm_price_button = None
        self.state_sold = None
        self.state_added_lab = None
        self.residual_lab = None
        self.wh_residual = None
        self.amount_for_wh = 0
        self.wh_good = None
        self.wh_good_container = []
        self.temp_amount = None
        self.selling_price = 0
        self.state_sold_entry = None
        self.state_added_entry = None
        self.machine_price_label = None
        self.machine_price_entry = None
        self.sold_amount_title = None
        self.sold_amount_entry = None
        self.confirm_sold_button = None

        self.row_counter = 0
        self.row_pos = 0

        self.main_color = "green2"
        self.machine_header = tk.Frame(self.workspace, width=self.width - 28, height=self.height / 8, bg="gray12")
        self.machine_header.grid(row=0, column=0, columnspan=3)
        self.title_lab = tk.Label(self.machine_header, text=name, font="Arial 20 bold", bg="gray12", fg=self.main_color, width=15)
        self.title_lab.grid(row=0, column=0, ipady=10, padx=4)
        self.machine_worth_lab = tk.Label(self.machine_header, text='Hodnota v automate: ', font="Arial 17 bold", bg="gray12", fg=self.main_color, width=55, anchor='e')
        self.machine_worth_lab.grid(row=0, column=1, ipady=12.5, sticky="WE")
        self.worth_lab = tk.Label(self.machine_header, text=self.machine_worth, font="Arial 17 bold", bg="gray12", fg=self.main_color, width=13)
        self.worth_lab.grid(row=0, column=2)
        self.machine_frame = tk.Frame(self.workspace, width=700, height=748, bg="gray2")
        self.machine_frame.grid(row=1, column=0, pady=2, padx=2, ipadx=128, sticky="NSW")
        self.machine_frame.columnconfigure(5, weight=1)
        self.machine_item_title = tk.Label(self.machine_frame, text="Tovar", width=15, font="Arial 14", fg="white", bg="gray22")
        self.machine_item_title.grid(row=0, column=0, padx=4, pady=4, sticky="NSWE")
        self.machine_price_title = tk.Label(self.machine_frame, text="Pred.cena", width=10, font="Arial 14", fg="white", bg="gray22")
        self.machine_price_title.grid(row=0, column=1, padx=4, pady=4, sticky="NSWE")
        self.machine_amount_title = tk.Label(self.machine_frame, text="Počet kusov", width=10, font="Arial 14", fg="white", bg="gray22")
        self.machine_amount_title.grid(row=0, column=2, padx=4, pady=4, sticky="NSWE")
        # Machine button frame
        self.machine_button_frame = tk.Frame(self.workspace, width=300, height=748, bg="gray22")
        self.machine_button_frame.grid(row=1, column=1, rowspan=200, pady=2, padx=2, ipadx=20, ipady=284, sticky="NSE")
        self.add_good_button = tk.Button(self.machine_button_frame, text="Doplniť automat", command=self.pull_warehouse, font="Arial 12 bold", bg="gray26", fg="white")
        self.add_good_button.grid(row=0, column=0, padx=40, pady=6, ipadx=110, sticky="WE")
        self.sold_goods_button = tk.Button(self.machine_button_frame, text="Zadať predané", command=self.open_sold_entries, font="Arial 12 bold", bg="gray26", fg="white")
        self.sold_goods_button.grid(row=1, column=0, padx=40, pady=6, ipadx=110, sticky="WE")
        self.set_price_button = tk.Button(self.machine_button_frame, text="Nastaviť ceny", command=self.change_prices, font="Arial 12 bold", bg="gray26", fg="white")
        self.set_price_button.grid(row=2, column=0, padx=40, pady=6, ipadx=110, sticky="WE")
        self.storno_button = tk.Button(self.machine_button_frame, text="Storno tovaru", command=self.open_storno_entries, font="Arial 12 bold", bg="gray26", fg="white")
        self.storno_button.grid(row=3, column=0, padx=40, pady=6, ipadx=110, sticky="WE")
        self.move_to_wh_button = tk.Button(self.machine_button_frame, text="Automat --> Sklad", command=self.open_wh_entries, font="Arial 12 bold", bg="gray26", fg="white")
        self.move_to_wh_button.grid(row=4, column=0, padx=40, pady=6, ipadx=110, sticky="WE")
        self.filter_button = tk.Button(self.machine_button_frame, text="Filtrovať", font="Arial 12 bold", bg="gray26", fg="white")
        self.filter_button.grid(row=5, column=0, padx=40, pady=6, ipadx=110, sticky="WE")

    def refresh_machine_state(self):
        self.wh_stack = self.load_warehouse()
        self.calculate_machine()
        self.machine_content = db.refresh_db("tovar", "vending_db." + self.machine)
        for idx, good in enumerate(set(self.machine_content)):
            good = good[0]
            good_db = "'" + good + "'"
            self.machine_content2 = db.refresh_db("predajna_cena, sum(pocet_kusov)", "vending_db." + self.machine, "tovar = " + good_db)
            self.row_pos = 2
            for x in self.machine_content2:
                price, summed_amount = x
                self.machine_good = tk.Label(self.machine_frame, text=good, font="Arial 12", fg="white", bg="gray2")
                self.machine_good.grid(row=self.row_pos + idx, column=0, pady=1, padx=1)
                self.machine_price = tk.Label(self.machine_frame, text=price, font="Arial 12", fg="white", bg="gray2")
                self.machine_price.grid(row=self.row_pos + idx, column=1, pady=1, padx=1)
                self.machine_amount = tk.Label(self.machine_frame, text=summed_amount, font="Arial 12", fg="white", bg="gray2")
                self.machine_amount.grid(row=self.row_pos + idx, column=2, pady=1, padx=1)
                self.machine_prices_container.append([good, price, "empty", "empty2"])
                self.machine_prices_check[good] = price

        return self.machine_prices_container, self.machine_prices_check, self.wh_stack

    def load_warehouse(self, from_where=None):
        self.wh = {}
        if from_where:
            self.wh = {}
            self.wh_stocks = db.refresh_db("*", from_where)
            for x in self.wh_stocks:
                good, cost, selling_price, amount = x
                if good not in self.wh.keys():
                    self.wh[good] = deque()
                    enqueue(self.wh[good], [cost, selling_price, amount])
                elif good in self.wh.keys():
                    for y in range(len(self.wh[good])):
                        if self.wh[good][y][0] == cost:
                            self.aux_wh = y
                            break
                        elif self.wh[good][y][0] != cost:
                            pass
                    if self.aux_wh:
                        self.wh[good][self.aux_wh][2] += amount
                    else:
                        enqueue(self.wh[good], [cost, selling_price, amount])

            return self.wh
        else:
            self.wh_stocks = db.refresh_db("*", "vending_db.sklad")
            for x in self.wh_stocks:
                good, cost, amount = x
                if good not in self.wh.keys():
                    self.wh[good] = deque()
                    enqueue(self.wh[good], [cost, amount])
                elif good in self.wh.keys():
                    for y in range(len(self.wh[good])):
                        if self.wh[good][y][0] == cost:
                            self.aux_wh = y
                            break
                        elif self.wh[good][y][0] != cost:
                            pass
                    if self.aux_wh:
                        self.wh[good][self.aux_wh][1] += amount
                    else:
                        enqueue(self.wh[good], [cost, amount])

            return self.wh

    def calculate_machine(self):
        self.machine_worth = db.make_sum("cena_s_dph * pocet_kusov", "vending_db." + self.machine)[0][0]
        if self.machine_worth is None:
            self.worth_lab.config(text=str(0) + " €")
        else:
            self.worth_lab.config(text=str(round(self.machine_worth, 2)) + " €")

    def pull_warehouse(self):
        self.wh_good_container = []
        self.wh_stocks = []
        self.wh_stack = {}
        self.machine_top = tk.Toplevel(self.workspace, bg="gray22")
        self.machine_top.geometry("840x930")
        self.machine_top.protocol("WM_DELETE_WINDOW", self.close_machine_top)
        self.machine_date_lab = tk.Label(self.machine_top, text="Dátum doplnenia automatu: ", font="Arial 14 bold", bg="gray26", fg="white")
        self.machine_date_lab.grid(row=0, column=4, padx=10, pady=6)
        self.machine_date = DateEntry(self.machine_top, date_pattern='yyyy-mm-dd')
        self.machine_date.grid(row=0, column=5, padx=10, pady=4)
        self.good_lab = tk.Label(self.machine_top, text="Tovar", width=10, font="Arial 14", fg="white", bg="gray26")
        self.good_lab.grid(row=0, column=0, padx=10, pady=4)
        self.residual_lab = tk.Label(self.machine_top, text="Zostatok", width=10, font="Arial 14", fg="white", bg="gray26")
        self.residual_lab.grid(row=0, column=1, padx=10, pady=4)
        self.state_added_lab = tk.Label(self.machine_top, text="Počet kusov", width=10, font="Arial 14", fg="white", bg="gray26")
        self.state_added_lab.grid(row=0, column=2, padx=10, pady=4)
        tk.Button(self.machine_top, text="Potvrdiť", width=30, command=self.move_from_wh, font="Arial 12 bold", bg="gray26", fg="white").grid(row=1, column=4, columnspan=2)
        self.wh_stack = self.load_warehouse()
        self.wh_stocks = db.refresh_db("tovar", "vending_db.sklad")
        for idx, good in enumerate(set(self.wh_stocks)):
            good = good[0]
            self.temp_amount = sum([self.wh_stack[good][a][1] for a in range(len(self.wh_stack[good]))])
            self.wh_good = tk.Label(self.machine_top, text=good, anchor="w", font="Arial 10", bg="gray22", fg="white")
            self.wh_good.grid(row=idx + 1, column=0, pady=2, padx=1)
            self.wh_residual = tk.Label(self.machine_top, text=self.temp_amount, anchor="w", font="Arial 10", bg="gray22", fg="white")
            self.wh_residual.grid(row=idx + 1, column=1, pady=2, padx=1)
            self.state_added_entry = tk.Entry(self.machine_top, width=10)
            self.state_added_entry.grid(row=idx + 1, column=2)
            self.row_counter = idx + 1
            self.wh_good_container.append((good, self.state_added_entry))
        return self.wh_good_container, self.wh_stack

    @staticmethod
    def print_message(title, body):
        messagebox.showinfo(title, body)

    def move_from_wh(self):
        self.wh_stack = self.load_warehouse()
        self.temp_amount = 0
        for x in self.wh_good_container:
            good, pull_entry = x
            pulled_amount = pull_entry.get()
            self.temp_amount = sum([self.wh_stack[good][a][1] for a in range(len(self.wh_stack[good]))])
            if len(pulled_amount) == 0:
                pass
            elif not pulled_amount.isdigit():
                self.print_message("Nevalidný vstup", f'Pre položku {good} ste nezadali číselnú hodnotu')
                continue
            elif int(pulled_amount) > self.temp_amount:
                self.print_message("Upozornenie", f'Zostávajúci počet kusov položky {good} je: {self.temp_amount}')
                continue
            else:
                if good not in self.machine_prices_check.keys() or self.machine_prices_check[good] is None:
                    print("With selling price")
                    self.selling_price = simpledialog.askstring("Nastav cenu", f'Zadaj predajnú cenu pre {good}: ')
                    self.selling_price = transform_str(self.selling_price)
                    while pulled_amount != 0:
                        cost = self.wh_stack[good][0][0]
                        pulled_amount = int(pulled_amount)
                        if pulled_amount <= self.wh_stack[good][0][1]:
                            self.aux = self.wh_stack[good][0][1] - pulled_amount
                            db.insert_db('vending_db.' + self.machine, "(tovar, cena_s_dph, predajna_cena, pocet_kusov)", str((good, cost, self.selling_price, pulled_amount)),
                                         "pocet_kusov = pocet_kusov + " + str(pulled_amount))
                            db.insert_db('vending_db.' + self.machine + "_predaje", "(datum, tovar, cena_s_dph, predajna_cena, pocet_kusov, status)",
                                         str((self.machine_date.get(), good, cost, self.selling_price, pulled_amount, "D")))
                            db.insert_db('vending_db.sklad', "(tovar, cena_s_dph, pocet_kusov)", str((good, cost, pulled_amount)), "pocet_kusov = pocet_kusov - " + str(pulled_amount))
                            if self.aux == 0:
                                dequeue(self.wh_stack[good])
                            pulled_amount = 0
                        elif pulled_amount > self.wh_stack[good][0][1]:
                            db.insert_db('vending_db.' + self.machine, "(tovar, cena_s_dph, predajna_cena, pocet_kusov)", str((good, cost, self.selling_price, self.wh_stack[good][0][1])),
                                         "pocet_kusov = pocet_kusov + " + str(self.wh_stack[good][0][1]))
                            db.insert_db('vending_db.' + self.machine + "_predaje", "(datum, tovar, cena_s_dph, predajna_cena, pocet_kusov, status)",
                                         str((self.machine_date.get(), good, cost, self.selling_price, self.wh_stack[good][0][1], "D")))
                            db.insert_db('vending_db.sklad', "(tovar, cena_s_dph, pocet_kusov)", str((good, cost, self.wh_stack[good][0][1])),
                                         "pocet_kusov = pocet_kusov - " + str(self.wh_stack[good][0][1]))
                            pulled_amount -= self.wh_stack[good][0][1]
                            dequeue(self.wh_stack[good])
                else:
                    while pulled_amount != 0:
                        pulled_amount = int(pulled_amount)
                        cost = self.wh_stack[good][0][0]
                        if pulled_amount <= self.wh_stack[good][0][1]:
                            self.aux = self.wh_stack[good][0][1] - pulled_amount
                            db.insert_db('vending_db.' + self.machine, "(tovar, cena_s_dph, pocet_kusov)", str((good, cost, pulled_amount)),
                                         "pocet_kusov = pocet_kusov + " + str(pulled_amount))
                            db.insert_db('vending_db.' + self.machine + "_predaje", "(datum, tovar, cena_s_dph, pocet_kusov, status)",
                                         str((self.machine_date.get(), good, cost, pulled_amount, "D")))
                            db.insert_db('vending_db.sklad', "(tovar, cena_s_dph, pocet_kusov)", str((good, cost, pulled_amount)), "pocet_kusov = pocet_kusov - " + str(pulled_amount))
                            if self.aux == 0:
                                dequeue(self.wh_stack[good])
                            pulled_amount = 0
                        elif pulled_amount > self.wh_stack[good][0][1]:
                            db.insert_db('vending_db.' + self.machine, "(tovar, cena_s_dph, pocet_kusov)", str((good, cost, self.wh_stack[good][0][1])),
                                         "pocet_kusov = pocet_kusov + " + str(self.wh_stack[good][0][1]))
                            db.insert_db('vending_db.' + self.machine + "_predaje", "(datum, tovar, cena_s_dph, pocet_kusov, status)",
                                         str((self.machine_date.get(), good, cost, self.wh_stack[good][0][1], "D")))
                            db.insert_db('vending_db.sklad', "(tovar, cena_s_dph, pocet_kusov)", str((good, cost, self.wh_stack[good][0][1])),
                                         "pocet_kusov = pocet_kusov - " + str(self.wh_stack[good][0][1]))
                            pulled_amount -= self.wh_stack[good][0][1]
                            dequeue(self.wh_stack[good])
        db.remove_from_db("vending_db.sklad", "pocet_kusov = 0")
        self.close_machine_top()
        self.machine_prices_container = []
        self.wh_stack = {}
        self.refresh_machine_state()

    def change_prices(self):
        self.add_good_button['state'] = tk.DISABLED
        self.sold_goods_button['state'] = tk.DISABLED
        self.storno_button['state'] = tk.DISABLED
        self.move_to_wh_button['state'] = tk.DISABLED
        self.filter_button['state'] = tk.DISABLED
        self.set_price_button.destroy()
        self.confirm_price_button = tk.Button(self.machine_button_frame, text="Potvrdiť ceny", command=self.lock_prices, font="Arial 12 bold", bg="gray26", fg="green2")
        self.confirm_price_button.grid(row=2, column=0, padx=40, pady=6, ipadx=110, sticky="WE")
        self.row_pos = 2
        for idx, y in enumerate(self.machine_prices_container):
            good, old_price, empty, empty2 = y
            self.machine_price_entry = tk.Entry(self.machine_frame, width=10)
            self.machine_price_entry.grid(row=self.row_pos + idx, column=1, pady=1, padx=1)
            self.machine_price_entry.insert(0, old_price)
            self.machine_prices_container[idx][2] = self.machine_price_entry

        return self.machine_prices_container

    def lock_prices(self):
        self.add_good_button['state'] = tk.ACTIVE
        self.sold_goods_button['state'] = tk.ACTIVE
        self.storno_button['state'] = tk.ACTIVE
        self.move_to_wh_button['state'] = tk.ACTIVE
        self.filter_button['state'] = tk.ACTIVE
        self.confirm_price_button.destroy()

        for idx, x in enumerate(self.machine_prices_container):
            good, old_price, price_widget, empty2 = x
            good = "'" + good + "'"
            price = transform_str(price_widget.get())
            db.update_db("vending_db." + self.machine, "predajna_cena", price, good)
            self.machine_prices_container[idx][2] = "empty"
            price_widget.destroy()

        self.set_price_button = tk.Button(self.machine_button_frame, text="Nastaviť ceny", command=self.change_prices, font="Arial 12 bold", bg="gray26", fg="white")
        self.set_price_button.grid(row=2, column=0, padx=40, pady=6, ipadx=110, sticky="WE")
        self.machine_prices_container = []
        self.refresh_machine_state()

    def open_sold_entries(self):
        self.machine_frame.grid_configure(ipadx=37)
        self.sold_goods_button.destroy()
        self.set_price_button['state'] = tk.DISABLED
        self.add_good_button['state'] = tk.DISABLED
        self.storno_button['state'] = tk.DISABLED
        self.move_to_wh_button['state'] = tk.DISABLED
        self.filter_button['state'] = tk.DISABLED
        self.confirm_sold_button = tk.Button(self.machine_button_frame, text="Potvrdiť predané", command=self.count_sold, font="Arial 12 bold", bg="gray26", fg="green2")
        self.confirm_sold_button.grid(row=1, column=0, padx=40, pady=6, ipadx=110, sticky="WE")
        self.sold_amount_title = tk.Label(self.machine_frame, text="Stav po predaji", width=15, font="Arial 14", fg="white", bg="gray22")
        self.sold_amount_title.grid(row=0, column=3, padx=4, pady=4, ipadx=2, sticky="NSWE")
        self.row_pos = 2
        for idx, x in enumerate(self.machine_prices_container):
            good, old_price, price_widget, empty2 = x
            self.sold_amount_entry = tk.Entry(self.machine_frame, width=10)
            self.sold_amount_entry.grid(row=self.row_pos + idx, column=3)
            self.machine_prices_container[idx][3] = self.sold_amount_entry

    def count_sold(self):
        self.wh_stack = {}
        self.sold_amount_title.destroy()
        self.machine_frame.grid_configure(ipadx=128)
        self.set_price_button['state'] = tk.ACTIVE
        self.add_good_button['state'] = tk.ACTIVE
        self.storno_button['state'] = tk.ACTIVE
        self.move_to_wh_button['state'] = tk.ACTIVE
        self.filter_button['state'] = tk.ACTIVE
        self.wh_stack = self.load_warehouse("vending_db." + self.machine)

        for idx, x in enumerate(self.machine_prices_container):
            good, old_price, price_widget, sold_widget = x
            sold = sold_widget.get()
            print(sold, "Initial sold")
            self.temp_amount = sum([self.wh_stack[good][a][2] for a in range(len(self.wh_stack[good]))])
            if len(sold_widget.get()) == 0:
                pass
            elif not sold.isdigit():
                self.print_message("Nevalidný vstup", f'Pre položku {good} ste nezadali číselnú hodnotu')
                continue
            elif int(sold) > self.temp_amount:
                self.print_message("Upozornenie", f'Zostávajúci počet kusov v automate z položky {good} je: {self.temp_amount}')
                continue
            else:
                sold = int(sold)
                while sold != 0:
                    # good_db = "'" + good + "'"
                    # self.machine_content2 = db.refresh_db("predajna_cena", "vending_db." + self.machine, "tovar = " + good_db)
                    cost = self.wh_stack[good][0][0]
                    selling_price = self.wh_stack[good][0][1]
                    if sold <= self.wh_stack[good][0][2]:
                        self.aux = self.wh_stack[good][0][2] - sold
                        print("sold:", sold, "warehouse:", self.wh_stack[good][0][2], "from sold < warehouse")
                        db.insert_db('vending_db.' + self.machine, "(tovar, cena_s_dph, predajna_cena, pocet_kusov)", str((good, cost, selling_price, sold)),
                                     "pocet_kusov = pocet_kusov - " + str(sold))
                        db.insert_db('vending_db.' + self.machine + "_predaje", "(datum, tovar, cena_s_dph, predajna_cena, pocet_kusov, status)",
                                     str((gui.selling_date, good, cost, selling_price, sold, "P")))
                        if self.aux == 0:
                            dequeue(self.wh_stack[good])
                        sold = 0
                    elif sold > self.wh_stack[good][0][2]:
                        print("sold:", sold, "warehouse:", self.wh_stack[good][0][2], "from sold > warehouse")
                        db.insert_db('vending_db.' + self.machine, "(tovar, cena_s_dph, predajna_cena, pocet_kusov)", str((good, cost, selling_price, self.wh_stack[good][0][2])),
                                     "pocet_kusov = pocet_kusov - " + str(self.wh_stack[good][0][2]))
                        db.insert_db('vending_db.' + self.machine + "_predaje", "(datum, tovar, cena_s_dph, predajna_cena, pocet_kusov, status)",
                                     str((gui.selling_date, good, cost, selling_price, self.wh_stack[good][0][2], "P")))
                        sold -= self.wh_stack[good][0][2]
                        dequeue(self.wh_stack[good])

            sold_widget.destroy()
        db.remove_from_db("vending_db." + self.machine, "pocet_kusov = 0")
        self.machine_prices_container = []
        self.wh_stack = {}
        self.refresh_machine_state()
        self.sold_goods_button = tk.Button(self.machine_button_frame, text="Zadať predané", command=self.open_sold_entries, font="Arial 12 bold", bg="gray26", fg="white")
        self.sold_goods_button.grid(row=1, column=0, padx=40, pady=6, ipadx=110, sticky="WE")

    def open_storno_entries(self):
        self.machine_frame.grid_configure(ipadx=37)
        self.storno_button.destroy()
        self.sold_goods_button['state'] = tk.DISABLED
        self.set_price_button['state'] = tk.DISABLED
        self.add_good_button['state'] = tk.DISABLED
        self.move_to_wh_button['state'] = tk.DISABLED
        self.filter_button['state'] = tk.DISABLED
        self.confirm_sold_button = tk.Button(self.machine_button_frame, text="Storno", command=self.storno_amount, font="Arial 12 bold", bg="gray26", fg="green2")
        self.confirm_sold_button.grid(row=3, column=0, padx=40, pady=6, ipadx=110, sticky="WE")
        self.sold_amount_title = tk.Label(self.machine_frame, text="Počet pre storno", width=15, font="Arial 14", fg="white", bg="gray22")
        self.sold_amount_title.grid(row=0, column=3, padx=4, pady=4, ipadx=2, sticky="NSWE")
        self.row_pos = 2
        for idx, x in enumerate(self.machine_prices_container):
            good, old_price, price_widget, empty2 = x
            self.sold_amount_entry = tk.Entry(self.machine_frame, width=10)
            self.sold_amount_entry.grid(row=self.row_pos + idx, column=3)
            self.machine_prices_container[idx][3] = self.sold_amount_entry

        return self.machine_prices_container

    def storno_amount(self):
        self.sold_amount_title.destroy()
        self.machine_frame.grid_configure(ipadx=128)
        self.sold_goods_button['state'] = tk.ACTIVE
        self.set_price_button['state'] = tk.ACTIVE
        self.add_good_button['state'] = tk.ACTIVE
        self.move_to_wh_button['state'] = tk.ACTIVE
        self.filter_button['state'] = tk.ACTIVE
        self.wh_stack = self.load_warehouse("vending_db." + self.machine)

        for idx, x in enumerate(self.machine_prices_container):
            good, old_price, price_widget, storno_widget = x
            sold = storno_widget.get()
            self.temp_amount = sum([self.wh_stack[good][a][2] for a in range(len(self.wh_stack[good]))])
            if len(storno_widget.get()) == 0:
                pass
            elif not sold.isdigit():
                self.print_message("Nevalidný vstup", f'Pre položku {good} ste nezadali číselnú hodnotu')
                continue
            elif int(sold) > self.temp_amount:
                self.print_message("Upozornenie", f'Zostávajúci počet kusov v automate z položky {good} je: {self.temp_amount}')
                continue
            else:
                sold = int(sold)
                while sold != 0:
                    cost = self.wh_stack[good][0][0]
                    good_db = "'" + good + "'"
                    self.machine_content2 = db.refresh_db("predajna_cena", "vending_db." + self.machine, "tovar = " + good_db)
                    selling_price = self.machine_content2[0][0]
                    if sold <= self.wh_stack[good][0][2]:
                        self.aux = self.wh_stack[good][0][2] - sold
                        db.insert_db('vending_db.' + self.machine, "(tovar, cena_s_dph, predajna_cena, pocet_kusov)", str((good, cost, selling_price, sold)),
                                     "pocet_kusov = pocet_kusov - " + str(sold))
                        db.insert_db('vending_db.' + self.machine + "_predaje", "(datum, tovar, cena_s_dph, predajna_cena, pocet_kusov, status)",
                                     str((gui.selling_date, good, cost, selling_price, sold, "S")))
                        if self.aux == 0:
                            dequeue(self.wh_stack[good])
                        sold = 0
                    elif sold > self.wh_stack[good][0][2]:
                        db.insert_db('vending_db.' + self.machine, "(tovar, cena_s_dph, predajna_cena, pocet_kusov)", str((good, cost, selling_price, self.wh_stack[good][0][2])),
                                     "pocet_kusov = pocet_kusov - " + str(self.wh_stack[good][0][2]))
                        db.insert_db('vending_db.' + self.machine + "_predaje", "(datum, tovar, cena_s_dph, predajna_cena, pocet_kusov, status)",
                                     str((gui.selling_date, good, cost, selling_price, self.wh_stack[good][0][2], "S")))
                        sold -= self.wh_stack[good][0][2]
                        dequeue(self.wh_stack[good])

            storno_widget.destroy()
        db.remove_from_db("vending_db." + self.machine, "pocet_kusov = 0")
        self.machine_prices_container = []
        self.wh_stack = {}
        self.refresh_machine_state()
        self.storno_button = tk.Button(self.machine_button_frame, text="Storno tovaru", command=self.open_storno_entries, font="Arial 12 bold", bg="gray26", fg="white")
        self.storno_button.grid(row=3, column=0, padx=40, pady=6, ipadx=110, sticky="WE")

        return self.machine_prices_container

    def open_wh_entries(self):
        self.machine_frame.grid_configure(ipadx=37)
        self.move_to_wh_button.destroy()
        self.sold_goods_button['state'] = tk.DISABLED
        self.set_price_button['state'] = tk.DISABLED
        self.add_good_button['state'] = tk.DISABLED
        self.storno_button['state'] = tk.DISABLED
        self.filter_button['state'] = tk.DISABLED
        self.confirm_sold_button = tk.Button(self.machine_button_frame, text="Presunúť do skladu", command=self.send_to_warehouse, font="Arial 12 bold", bg="gray26", fg="green2")
        self.confirm_sold_button.grid(row=4, column=0, padx=40, pady=6, ipadx=110, sticky="WE")
        self.sold_amount_title = tk.Label(self.machine_frame, text="Počet pre storno", width=15, font="Arial 14", fg="white", bg="gray22")
        self.sold_amount_title.grid(row=0, column=3, padx=4, pady=4, ipadx=2, sticky="NSWE")
        self.row_pos = 2
        for idx, x in enumerate(self.machine_prices_container):
            good, old_price, price_widget, empty2 = x
            self.sold_amount_entry = tk.Entry(self.machine_frame, width=10)
            self.sold_amount_entry.grid(row=self.row_pos + idx, column=3)
            self.machine_prices_container[idx][3] = self.sold_amount_entry

        return self.machine_prices_container

    def send_to_warehouse(self):
        self.sold_amount_title.destroy()
        self.machine_frame.grid_configure(ipadx=128)
        self.sold_goods_button['state'] = tk.ACTIVE
        self.set_price_button['state'] = tk.ACTIVE
        self.add_good_button['state'] = tk.ACTIVE
        self.storno_button['state'] = tk.ACTIVE
        self.filter_button['state'] = tk.ACTIVE
        self.wh_stack = self.load_warehouse("vending_db." + self.machine)

        for idx, x in enumerate(self.machine_prices_container):
            good, old_price, price_widget, storno_widget = x
            storno = storno_widget.get()
            self.temp_amount = sum([self.wh_stack[good][a][2] for a in range(len(self.wh_stack[good]))])
            if len(storno_widget.get()) == 0:
                pass
            elif not storno.isdigit():
                self.print_message("Nevalidný vstup", f'Pre položku {good} ste nezadali číselnú hodnotu')
                continue
            elif int(storno) > self.temp_amount:
                self.print_message("Upozornenie", f'Zostávajúci počet kusov v automate z položky {good} je: {self.temp_amount}')
                continue
            else:
                storno = int(storno)
                while storno != 0:
                    cost = self.wh_stack[good][0][0]
                    selling_price = self.wh_stack[good][0][1]
                    if storno <= self.wh_stack[good][0][2]:
                        self.aux = self.wh_stack[good][0][2] - storno
                        db.insert_db('vending_db.' + self.machine, "(tovar, cena_s_dph, predajna_cena, pocet_kusov)", str((good, cost, selling_price, storno)),
                                     "pocet_kusov = pocet_kusov - " + str(storno))
                        db.insert_db('vending_db.' + self.machine + "_predaje", "(datum, tovar, cena_s_dph, predajna_cena, pocet_kusov, status)",
                                     str((gui.selling_date, good, cost, selling_price, storno, "S")))
                        db.insert_db('vending_db.sklad', "(tovar, cena_s_dph, pocet_kusov)", str((good, cost, storno)),
                                     "pocet_kusov = pocet_kusov + " + str(storno))
                        if self.aux == 0:
                            dequeue(self.wh_stack[good])
                        storno = 0
                    elif storno > self.wh_stack[good][0][2]:
                        db.insert_db('vending_db.' + self.machine, "(tovar, cena_s_dph, predajna_cena, pocet_kusov)", str((good, cost, selling_price, self.wh_stack[good][0][2])),
                                     "pocet_kusov = pocet_kusov - " + str(self.wh_stack[good][0][2]))
                        db.insert_db('vending_db.' + self.machine + "_predaje", "(datum, tovar, cena_s_dph, predajna_cena, pocet_kusov, status)",
                                     str((gui.selling_date, good, cost, selling_price, self.wh_stack[good][0][2], "S")))
                        db.insert_db('vending_db.sklad', "(tovar, cena_s_dph, pocet_kusov)", str((good, cost, self.wh_stack[good][0][2])),
                                     "pocet_kusov = pocet_kusov + " + self.wh_stack[good][0][2])
                        storno -= self.wh_stack[good][0][2]
                        dequeue(self.wh_stack[good])

            storno_widget.destroy()
        db.remove_from_db("vending_db." + self.machine, "pocet_kusov = 0")
        self.machine_prices_container = []
        self.wh_stack = {}
        self.refresh_machine_state()
        self.move_to_wh_button = tk.Button(self.machine_button_frame, text="Automat --> Sklad", command=self.open_wh_entries, font="Arial 12 bold", bg="gray26", fg="white")
        self.move_to_wh_button.grid(row=4, column=0, padx=40, pady=6, ipadx=110, sticky="WE")

        return self.machine_prices_container

    def close_machine_top(self):
        self.machine_top.destroy()

    def run_machine(self):
        self.workspace.mainloop()


if __name__ == "__main__":
    gui = MainWorkspace('Vending Machine')
    gui.unpacking_dat()
    gui.initiate_base_state()
    gui.run()
