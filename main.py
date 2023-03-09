import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from time import strftime
# Subfiles
import database as db

# Frontend


class Abstract:
    def __init__(self, name):
        # Initializing of GUI
        self.workspace = tk.Tk()
        self.workspace.title(name)
        self.workspace.resizable(width=False, height=False)
        self.workspace.configure(bg="gray2")
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
            print(dat_machines)
            for machine in self.machine_container:
                machine = machine + "**"
                dat_machines.write(machine)

        # Vending machines

    def add_machine(self):
        self.new_name = simpledialog.askstring("Nový automat", "Zadaj názov automatu: ")
        if self.new_name:
            self.plus.destroy()
            self.machine_label = tk.Label(self.vending_area, text=self.new_name, font="Aerial 14 bold", bg="gray22", fg="white")
            self.machine_label.grid(row=self.ver_mover, column=self.hor_mover, padx=2, pady=20)
            self.vending_machine = tk.Button(self.vending_area, image=self.logo)
            self.vending_machine.grid(row=self.ver_mover+1, column=self.hor_mover, padx=90)
            self.machine_container.append(self.machine_label.cget("text"))
            db.create_table(self.new_name)
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
        print(self.machine_container, len(self.machine_container))
        if len(self.machine_container) != 0:
            for machine in self.machine_container:
                self.plus.destroy()
                self.machine_label = tk.Label(self.vending_area, text=machine, font="Aerial 14 bold", bg="gray22", fg="white")
                self.machine_label.grid(row=self.ver_mover, column=self.hor_mover, padx=2, pady=20)
                self.vending_machine = tk.Button(self.vending_area, image=self.logo)
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

    def open_machine(self, machine_name):
        machine_name = VendingMachine(machine_name)
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
        self.add_button = tk.Button(self.wh_workspace, text='Znížiť stav', font="Arial 12 bold", bg="gray26", fg="white")
        self.add_button.grid(row=2, column=4, columnspan=2, padx=10, pady=4, ipadx=100, sticky="NEW")

        # Autoload
        self.new_purchase = None
        self.good_label = None
        self.price_label = None
        self.refundable_label = None
        self.amount_label = None
        self.price_w_ref = 0

        self.wh_items = set()
        self.wh_result = []
        self.good_name_cont = []
        self.purchase_cont = []
        self.refundable_vars = []
        self.name_of_good = None
        self.price_entry = None
        self.refundable_check = None
        self.amount_entry = None
        self.ref_var = tk.IntVar(self.new_purchase, value=0)
        self.row_counter = 0
        self.plus_row = None
        self.temp = 0
        self.new_good = None

    @staticmethod
    def transform_str(string):
        return string.replace(",", ".")

    def calculate_wh(self):
        self.wh_worth = db.make_sum()[0][0]
        print(self.wh_worth, "Here")
        self.wh_state.config(text=str(round(self.wh_worth, 2)) + " €")

    def refresh_state(self):
        self.calculate_wh()
        for y in self.wh_table.get_children():
            self.wh_table.delete(y)
        self.wh_result = db.refresh_db("*")
        for x in self.wh_result:
            item, price, amount = x
            self.wh_table.insert('', 'end', values=(str(item), str(price), str(amount)))
            self.wh_items.add(str(x[0]))

    def make_purchase(self):
        for idx, item in enumerate(self.good_name_cont):
            temp_item = "'" + item + "'"
            print(temp_item)
            price, amount, var = self.purchase_cont[idx]
            self.temp = db.refresh_db("*", str(temp_item))
            if item not in self.wh_items:
                print("Insert")
                if var.get() == 0:
                    db.insert_db("vending_db.sklad", "(tovar, cena_s_dph, pocet_kusov)", str((item, float(price.get().replace(",", ".")), amount.get().replace(",", "."))))
                elif var.get() == 1:
                    self.price_w_ref = float(price.get().replace(",", ".")) + 0.15
                    db.insert_db("vending_db.sklad", "(tovar, cena_s_dph, pocet_kusov)", str((item, self.price_w_ref, amount.get().replace(",", "."))))
            elif item in self.wh_items:
                print("update")
                for n in self.temp:
                    n_item, n_price, n_amount = n
                    if len(price.get().replace(",", ".")) == 0 or len(amount.get().replace(",", ".")) == 0:
                        print("Nothing happend")
                    elif n_price == float(price.get().replace(",", ".")):
                        print("update with same prices")
                        db.update_db("vending_db.sklad", "pocet_kusov", n_amount + int(amount.get().replace(",", ".")), temp_item, float(price.get().replace(",", ".")))
                    elif n_price != float(price.get().replace(",", ".")):
                        print("update with different prices")
                        db.insert_db("vending_db.sklad", "(tovar, cena_s_dph, pocet_kusov)", str((item, price.get().replace(",", "."), amount.get().replace(",", "."))))

    def add_goods(self):
        self.wh_result = db.refresh_db("tovar")
        self.new_purchase = tk.Toplevel(self.wh_workspace, bg="gray22")
        self.new_purchase.geometry("800x800")
        self.new_purchase.protocol("WM_DELETE_WINDOW", self.close_toplevel)
        self.good_label = tk.Label(self.new_purchase, text="Tovar", font="Arial 11", fg="white", bg="gray26")
        self.good_label.grid(row=0, column=0, padx=10, pady=4)
        self.price_label = tk.Label(self.new_purchase, text="Nák. cena s DPH", font="Arial 11", fg="white", bg="gray26")
        self.price_label.grid(row=0, column=1, padx=10, pady=4)
        self.amount_label = tk.Label(self.new_purchase, text="Množstvo", font="Arial 11", fg="white", bg="gray26")
        self.amount_label.grid(row=0, column=2, padx=10, pady=4)
        self.refundable_label = tk.Label(self.new_purchase, text="Zálohovanie", font="Arial 11", fg="white", bg="gray26")
        self.refundable_label.grid(row=0, column=3, padx=10, pady=4)
        tk.Button(self.new_purchase, text="Potvrdiť", command=self.make_purchase, font="Arial 12 bold", bg="gray26", fg="white").grid(row=1, column=4, columnspan=3, sticky="WE")
        for idx, tovar in enumerate(set(self.wh_result)):
            self.name_of_good = tk.Label(self.new_purchase, text=tovar, anchor="w", font="Arial 10", bg="gray22", fg="white")
            self.name_of_good.grid(row=idx + 1, column=0, pady=8, padx=2)
            self.good_name_cont.append(self.name_of_good.cget('text'))
            self.price_entry = tk.Entry(self.new_purchase, width=8)
            self.price_entry.grid(row=idx + 1, column=1)
            self.amount_entry = tk.Entry(self.new_purchase, width=8)
            self.amount_entry.grid(row=idx + 1, column=2)
            self.ref_var = tk.IntVar(self.new_purchase, value=0)
            self.refundable_check = tk.Checkbutton(self.new_purchase, variable=self.ref_var, onvalue=1, offvalue=0, bg="gray26")
            self.refundable_check.grid(row=idx + 1, column=3)
            self.purchase_cont.append((self.price_entry, self.amount_entry, self.ref_var))
            self.row_counter += 1
        self.plus_row = tk.Button(self.new_purchase, text="+", command=self.add_new_good, anchor="w", font="Arial 10", bg="gray22", fg="white")
        self.plus_row.grid(row=self.row_counter + 1, column=0)

    def add_new_good(self):
        self.new_good = simpledialog.askstring("Nový tovar", "Zadaj názov tovaru: ")
        if self.new_good:
            self.plus_row.destroy()
            self.name_of_good = tk.Label(self.new_purchase, text=self.new_good, anchor="w", font="Arial 10", bg="gray22", fg="white")
            self.name_of_good.grid(row=self.row_counter + 1, column=0, pady=8, padx=2)
            self.good_name_cont.append(self.name_of_good.cget('text'))
            self.price_entry = tk.Entry(self.new_purchase, width=8)
            self.price_entry.grid(row=self.row_counter + 1, column=1)
            self.amount_entry = tk.Entry(self.new_purchase, width=8)
            self.amount_entry.grid(row=self.row_counter + 1, column=2)
            self.ref_var = tk.IntVar(self.new_purchase, value=0)
            self.refundable_check = tk.Checkbutton(self.new_purchase, variable=self.ref_var, onvalue=1, offvalue=0, bg="gray26")
            self.refundable_check.grid(row=self.row_counter + 1, column=3)
            self.purchase_cont.append((self.price_entry, self.amount_entry, self.ref_var))
            self.row_counter += 1
            self.plus_row = tk.Button(self.new_purchase, text="+", command=self.add_new_good, anchor="w", font="Arial 10", bg="gray22", fg="white")
            self.plus_row.grid(row=self.row_counter + 1, column=0)

    def close_toplevel(self):
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

    def run_machine(self):
        self.workspace.mainloop()


if __name__ == "__main__":
    gui = MainWorkspace('Vending Machine')
    gui.unpacking_dat()
    gui.initiate_base_state()
    gui.run()
