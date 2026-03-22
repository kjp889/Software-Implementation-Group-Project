import tkinter as tk
from tkinter import messagebox
import mysql.connector
import numpy as np

dbAccess = mysql.connector.connect(host="localhost", user="root", password="", database="SoftwareImplementation")

if dbAccess.is_connected():
    print("Connected")
else:
    print("Not Connected")
    dbAccess.close()

class LogIn:
    
    def __init__(self):
        self.window = tk.Tk()
        
        #self.window.protocol("WM_DELETE_WINDOW", self.onClose)

        self.window.geometry("900x500")
        self.window.title("Login")

        self.login_Frame = tk.Frame(self.window)
        self.login_Frame.columnconfigure(0, weight=1)
        self.login_Frame.columnconfigure(1, weight=1)

        self.login_Label = tk.Label(self.window, text="Login", font=("Arial", 18))
        self.login_Label.pack(pady=20)

        self.usr_label = tk.Label(self.login_Frame, text="Username: ", font=("Arial", 12))
        self.usr_label.grid(row=0,column=0,sticky=tk.W+tk.E)

        self.usr_Entry = tk.Entry(self.login_Frame)
        self.usr_Entry.grid(row=0,column=1,sticky=tk.W+tk.E)

        self.pwd_label = tk.Label(self.login_Frame, text="Password: ", font=("Arial", 12))
        self.pwd_label.grid(row=1,column=0,sticky=tk.W+tk.E)

        self.pwd_Entry = tk.Entry(self.login_Frame,show="*")
        self.pwd_Entry.bind("<KeyPress>", self.onPressReturn)
        self.pwd_Entry.grid(row=1,column=1,sticky=tk.W+tk.E)

        self.login_Frame.pack()
        
        self.login_Button=tk.Button(self.window,text="Login",command=self.onLoginClick)
        self.login_Button.pack()
        

        self.window.mainloop()
        
    def onLoginClick(self):
        print(self.usr_Entry.get())
        self.loginVerification()
        
    
    def loginVerification(self):
        self.usr = self.usr_Entry.get()
        self.pwd = self.pwd_Entry.get()
        
        self.cursor = dbAccess.cursor()
        self.cursor.execute("SELECT * FROM user WHERE user_name = %s AND password = %s", (self.usr, self.pwd))
        self.result = self.cursor.fetchone()
        
        if self.result is not None:
            self.window.destroy()
            ManagerSub()
        else:
            messagebox.showerror("Error", "Invalid Username or Password")
        
    def onPressReturn(self, event):
        if event.keysym == "Return":
            self.onLoginClick()

class ManagerSub:
    
    def __init__(self):
        self.windowManager = tk.Tk()

        self.windowManager.geometry("900x500")
        self.windowManager.title("Manager")
        
        self.menuLayout()
        
        self.displayScreen()
        
        self.windowManager.mainloop()
        
    def logOut(self):
        self.windowManager.destroy()
        LogIn()
    
    def gotoInventory(self):
        self.windowManager.destroy()
        InventoryView()
    
    def gotoReports(self):
        self.windowManager.destroy()
        ReportsView()
    
    def gotoOrderTracking(self):
        self.windowManager.destroy()
        OrderTrackingView()
    
    def gotoPurchases(self):
        self.windowManager.destroy()
        PurchasesView()
    
    def gotoInventoryUpdate(self):
        self.windowManager.destroy()
        InventoryUpdateView()
    
    def gotoAddItem(self):
        self.windowManager.destroy()
        AddItemView()
    
    def home(self):
        self.windowManager.destroy()
        ManagerSub()
        
    def menuLayout(self):
        self.menuBar = tk.Menu(self.windowManager)
        self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
        self.reportMenu = tk.Menu(self.menuBar, tearoff=0)
        self.inventoryMenu =tk.Menu(self.menuBar, tearoff=0)
        self.salesMenu = tk.Menu(self.menuBar, tearoff=0)
        self.reportGen = tk.Menu(self.menuBar, tearoff=0)
        
        self.menuBar.add_cascade(menu=self.fileMenu, label="File")
        self.menuBar.add_cascade(menu=self.reportMenu, label="Report")
        self.menuBar.add_cascade(menu=self.inventoryMenu, label="Inventory")
        self.menuBar.add_cascade(menu=self.salesMenu, label="Sales")
        
        self.fileMenu.add_command(label="LogOut", command=self.logOut)
        self.fileMenu.add_command(label="Dashboard", command=self.home)
        
        self.reportMenu.add_cascade(label="Generate Report", menu=self.reportGen, command=self.gotoReports)
        self.reportGen.add_command(label="Monthly Sales Report", command=self.reps)
        self.reportGen.add_command(label="Annual Sales Report", command=self.reps)
        self.reportGen.add_command(label="Inventory Report", command=self.reps)
        self.reportGen.add_command(label="Customer Report", command=self.reps)
        
        self.inventoryMenu.add_command(label="Add Item", command=self.gotoAddItem)
        self.inventoryMenu.add_command(label="Update Stock", command=self.gotoInventoryUpdate)
        self.inventoryMenu.add_command(label="Review Stock", command=self.gotoInventory)
        
        self.salesMenu.add_command(label="Review Sale", command=self.gotoPurchases)
        self.salesMenu.add_separator()
        self.salesMenu.add_command(label="Track Order", command=self.gotoOrderTracking)
                
        self.windowManager.config(menu=self.menuBar)

    def displayScreen(self):
        self.display_Frame = tk.Frame(self.windowManager)
        self.display_Frame.columnconfigure(0, weight=1)
        self.display_Frame.columnconfigure(1, weight=1)
        
        self.checkInventoryBtn = tk.Button(self.display_Frame,text="Check Inventory", command=self.gotoInventory, border=1)
        self.checkInventoryBtn.grid(row=0,column=0,sticky=tk.W+tk.E)
        
        self.updateInventoryBtn = tk.Button(self.display_Frame,text="Add Item", command=self.gotoAddItem, border=1)
        self.updateInventoryBtn.grid(row=0,column=1,sticky=tk.W+tk.E)
        
        self.purchaseReviewBtn = tk.Button(self.display_Frame,text="Review Purchases", command=self.gotoPurchases, border=1)
        self.purchaseReviewBtn.grid(row=1,column=0,sticky=tk.W+tk.E)
        
        self.reportBtn = tk.Button(self.display_Frame,text="Generate Report", command=self.gotoReports, border=1)
        self.reportBtn.grid(row=1,column=1,sticky=tk.W+tk.E)
        
        self.display_Frame.pack()
        
        self.trackingBtn = tk.Button(self.windowManager,text="Track Order", command=self.gotoOrderTracking, border=1)
        self.trackingBtn.pack()

    def reps(self):
        messagebox.showerror("Report Generating Error", "Unable to Generate Report at the moment")

class InventoryView:
    
    def __init__(self):
        self.windowManager = tk.Tk()

        self.windowManager.geometry("900x500")
        self.windowManager.title("Test")
        
        self.menuLayout()
        
        self.displayScreen()
        
        self.windowManager.mainloop()
        
    def logOut(self):
        self.windowManager.destroy()
        LogIn()
    
    def gotoInventory(self):
        self.windowManager.destroy()
        InventoryView()
    
    def gotoReports(self):
        self.windowManager.destroy()
        ReportsView()
    
    def gotoOrderTracking(self):
        self.windowManager.destroy()
        OrderTrackingView()
    
    def gotoPurchases(self):
        self.windowManager.destroy()
        PurchasesView()
    
    def gotoInventoryUpdate(self):
        self.windowManager.destroy()
        InventoryUpdateView()
    
    def gotoAddItem(self):
        self.windowManager.destroy()
        AddItemView()
    
    def home(self):
        self.windowManager.destroy()
        ManagerSub()
        
    def menuLayout(self):
        self.menuBar = tk.Menu(self.windowManager)
        self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
        self.reportMenu = tk.Menu(self.menuBar, tearoff=0)
        self.inventoryMenu =tk.Menu(self.menuBar, tearoff=0)
        self.salesMenu = tk.Menu(self.menuBar, tearoff=0)
        self.reportGen = tk.Menu(self.menuBar, tearoff=0)
        
        self.menuBar.add_cascade(menu=self.fileMenu, label="File")
        self.menuBar.add_cascade(menu=self.reportMenu, label="Report")
        self.menuBar.add_cascade(menu=self.inventoryMenu, label="Inventory")
        self.menuBar.add_cascade(menu=self.salesMenu, label="Sales")
        
        self.fileMenu.add_command(label="LogOut", command=self.logOut)
        self.fileMenu.add_command(label="Dashboard", command=self.home)
        
        self.reportMenu.add_cascade(label="Generate Report", menu=self.reportGen, command=self.gotoReports)
        self.reportGen.add_command(label="Monthly Sales Report", command=self.reps)
        self.reportGen.add_command(label="Annual Sales Report", command=self.reps)
        self.reportGen.add_command(label="Inventory Report", command=self.reps)
        self.reportGen.add_command(label="Customer Report", command=self.reps)
        
        self.inventoryMenu.add_command(label="Add Item", command=self.gotoAddItem)
        self.inventoryMenu.add_command(label="Update Stock", command=self.gotoInventoryUpdate)
        self.inventoryMenu.add_command(label="Review Stock", command=self.gotoInventory)
        
        self.salesMenu.add_command(label="Review Sale", command=self.gotoPurchases)
        self.salesMenu.add_separator()
        self.salesMenu.add_command(label="Track Order", command=self.gotoOrderTracking)
                
        self.windowManager.config(menu=self.menuBar)

    def displayScreen(self):
        #array = np.array([[100, 1, 2, 3, 4, 5, ''],[6, 7, 8, 9, 10, 11, ''],[12, 13, 14, 15, 16, 17, ''],[18, 19, 20, 21, 22, 23, '']])
        
        self.cursor = dbAccess.cursor()
        self.cursor.execute("SELECT `item_code`, `item_name`, `descpri`, `price`, `qty_on_hand` FROM inventory")
        self.result = self.cursor.fetchall()
        
        self.display_Frame = tk.Frame(self.windowManager)
        self.display_Frame.columnconfigure(0, weight=1)
        self.display_Frame.columnconfigure(1, weight=1)
        self.display_Frame.columnconfigure(2, weight=1)
        self.display_Frame.columnconfigure(3, weight=1)
        self.display_Frame.columnconfigure(4, weight=1)
        self.display_Frame.columnconfigure(5, weight=1)
        
        self.headingItemID = tk.Label(self.display_Frame, text="Item Code", border=2)
        self.headingItemID.grid(row=0,column=0,sticky=tk.W+tk.E)
        
        self.headingItemName = tk.Label(self.display_Frame, text="Item Name", border=2)
        self.headingItemName.grid(row=0,column=1,sticky=tk.W+tk.E)
        
        self.headingItemDescription = tk.Label(self.display_Frame, text="Item Description", border=2)
        self.headingItemDescription.grid(row=0,column=2,sticky=tk.W+tk.E)
        
        self.headingPrice = tk.Label(self.display_Frame, text="Price", border=2)
        self.headingPrice.grid(row=0,column=3,sticky=tk.W+tk.E)
                
        self.headingQty = tk.Label(self.display_Frame, text="Quantity on Hand", border=2)
        self.headingQty.grid(row=0,column=4,sticky=tk.W+tk.E)
        
        for row_num, row in enumerate(self.result):
            #print(row_num, row)
            for col_num, col in enumerate(row):
                print(f"({row_num}, {col_num}) -> {col}")
                
                if col_num == 4:
                    self.dataBtn = tk.Button(self.display_Frame, text="Update", command=self.gotoInventoryUpdate)
                    self.dataBtn.grid(row=row_num+1,column=col_num+1,sticky=tk.W+tk.E)
                    self.data = tk.Label(self.display_Frame, text=col)
                    self.data.grid(row=row_num+1,column=col_num,sticky=tk.W+tk.E)
                else: 
                    self.data = tk.Label(self.display_Frame, text=col)
                    self.data.grid(row=row_num+1,column=col_num,sticky=tk.W+tk.E)
                
        self.display_Frame.pack()

    def reps(self):
        messagebox.showerror("Report Generating Error", "Unable to Generate Report at the moment")
        

class ReportsView:
    
    def __init__(self):
        self.windowManager = tk.Tk()

        self.windowManager.geometry("900x500")
        self.windowManager.title("Test")
        
        self.menuLayout()
        
        self.displayScreen()
        
        self.windowManager.mainloop()
        
    def logOut(self):
        self.windowManager.destroy()
        LogIn()
    
    def gotoInventory(self):
        self.windowManager.destroy()
        InventoryView()
    
    def gotoReports(self):
        self.windowManager.destroy()
        ReportsView()
    
    def gotoOrderTracking(self):
        self.windowManager.destroy()
        OrderTrackingView()
    
    def gotoPurchases(self):
        self.windowManager.destroy()
        PurchasesView()
    
    def gotoInventoryUpdate(self):
        self.windowManager.destroy()
        InventoryUpdateView()
    
    def gotoAddItem(self):
        self.windowManager.destroy()
        AddItemView()
    
    def home(self):
        self.windowManager.destroy()
        ManagerSub()
        
    def menuLayout(self):
        self.menuBar = tk.Menu(self.windowManager)
        self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
        self.reportMenu = tk.Menu(self.menuBar, tearoff=0)
        self.inventoryMenu =tk.Menu(self.menuBar, tearoff=0)
        self.salesMenu = tk.Menu(self.menuBar, tearoff=0)
        self.reportGen = tk.Menu(self.menuBar, tearoff=0)
        
        self.menuBar.add_cascade(menu=self.fileMenu, label="File")
        self.menuBar.add_cascade(menu=self.reportMenu, label="Report")
        self.menuBar.add_cascade(menu=self.inventoryMenu, label="Inventory")
        self.menuBar.add_cascade(menu=self.salesMenu, label="Sales")
        
        self.fileMenu.add_commanrow
        self.fileMenu.add_command(label="Dashboard", command=self.home)
        
        self.reportMenu.add_cascade(label="Generate Report", menu=self.reportGen, command=self.gotoReports)
        self.reportGen.add_command(label="Monthly Sales Report", command=self.reps)
        self.reportGen.add_command(label="Annual Sales Report", command=self.reps)
        self.reportGen.add_command(label="Inventory Report", command=self.reps)
        self.reportGen.add_command(label="Customer Report", command=self.reps)
        
        self.inventoryMenu.add_command(label="Add Item", command=self.gotoAddItem)
        self.inventoryMenu.add_command(label="Update Stock", command=self.gotoInventoryUpdate)
        self.inventoryMenu.add_command(label="Review Stock", command=self.gotoInventory)
        
        self.salesMenu.add_command(label="Review Sale", command=self.gotoPurchases)
        self.salesMenu.add_separator()
        self.salesMenu.add_command(label="Track Order", command=self.gotoOrderTracking)
                
        self.windowManager.config(menu=self.menuBar)

    def displayScreen(self):
        self.display_Frame = tk.Frame(self.windowManager)
        self.display_Frame.columnconfigure(0, weight=1)
        self.display_Frame.columnconfigure(1, weight=1)
        
        self.checkInventoryBtn = tk.Button(self.display_Frame,text="Monthly Sales Report", command=self.reps, border=1)
        self.checkInventoryBtn.grid(row=0,column=0,sticky=tk.W+tk.E)
        
        self.updateInventoryBtn = tk.Button(self.display_Frame,text="Annual Sales Report", command=self.reps, border=1)
        self.updateInventoryBtn.grid(row=0,column=1,sticky=tk.W+tk.E)
        
        self.purchaseReviewBtn = tk.Button(self.display_Frame,text="Inventory Report", command=self.reps, border=1)
        self.purchaseReviewBtn.grid(row=1,column=0,sticky=tk.W+tk.E)
        
        self.reportBtn = tk.Button(self.display_Frame,text="Customer Report", command=self.reps, border=1)
        self.reportBtn.grid(row=1,column=1,sticky=tk.W+tk.E)
        
        self.display_Frame.pack()
        
    def reps(self):
        messagebox.showerror("Report Generating Error", "Unable to Generate Report at the moment")

class OrderTrackingView:
    
    def __init__(self):
        self.windowManager = tk.Tk()

        self.windowManager.geometry("900x500")
        self.windowManager.title("Test")
        
        self.menuLayout()
        
        self.displayScreen()
        
        self.windowManager.mainloop()
        
    def logOut(self):
        self.windowManager.destroy()
        LogIn()
    
    def gotoInventory(self):
        self.windowManager.destroy()
        InventoryView()
    
    def gotoReports(self):
        self.windowManager.destroy()
        ReportsView()
    
    def gotoOrderTracking(self):
        self.windowManager.destroy()
        OrderTrackingView()
    
    def gotoPurchases(self):
        self.windowManager.destroy()
        PurchasesView()
    
    def gotoInventoryUpdate(self):
        self.windowManager.destroy()
        InventoryUpdateView()
    
    def gotoAddItem(self):
        self.windowManager.destroy()
        AddItemView()

    def home(self):
        self.windowManager.destroy()
        ManagerSub()
        
    def menuLayout(self):
        self.menuBar = tk.Menu(self.windowManager)
        self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
        self.reportMenu = tk.Menu(self.menuBar, tearoff=0)
        self.inventoryMenu =tk.Menu(self.menuBar, tearoff=0)
        self.salesMenu = tk.Menu(self.menuBar, tearoff=0)
        self.reportGen = tk.Menu(self.menuBar, tearoff=0)
        
        self.menuBar.add_cascade(menu=self.fileMenu, label="File")
        self.menuBar.add_cascade(menu=self.reportMenu, label="Report")
        self.menuBar.add_cascade(menu=self.inventoryMenu, label="Inventory")
        self.menuBar.add_cascade(menu=self.salesMenu, label="Sales")
        
        self.fileMenu.add_command(label="LogOut", command=self.logOut)
        self.fileMenu.add_command(label="Dashboard", command=self.home)
        
        self.reportMenu.add_cascade(label="Generate Report", menu=self.reportGen, command=self.gotoReports)
        self.reportGen.add_command(label="Monthly Sales Report", command=self.reps)
        self.reportGen.add_command(label="Annual Sales Report", command=self.reps)
        self.reportGen.add_command(label="Inventory Report", command=self.reps)
        self.reportGen.add_command(label="Customer Report", command=self.reps)
        
        self.inventoryMenu.add_command(label="Add Item", command=self.gotoAddItem)
        self.inventoryMenu.add_command(label="Update Stock", command=self.gotoInventoryUpdate)
        self.inventoryMenu.add_command(label="Review Stock", command=self.gotoInventory)
        
        self.salesMenu.add_command(label="Review Sale", command=self.gotoPurchases)
        self.salesMenu.add_separator()
        self.salesMenu.add_command(label="Track Order", command=self.gotoOrderTracking)
                
        self.windowManager.config(menu=self.menuBar)

    def displayScreen(self):
                
        self.cursor = dbAccess.cursor()
        self.cursor.execute("SELECT `invoice_num`, `tracking_num`, `location` FROM sales")
        self.result = self.cursor.fetchall()
        
        '''self.display_Frame = tk.Frame(self.windowManager)
        self.display_Frame.columnconfigure(0, weight=1)
        self.display_Frame.columnconfigure(1, weight=1)
        
        self.searchEntry = tk.Entry(self.display_Frame,)
        self.searchEntry.grid(row=0,column=0,sticky=tk.W+tk.E)
        
        self.searchBtn = tk.Button(self.display_Frame,text="Search", command=self.trackingSearch, border=1)
        self.searchBtn.grid(row=0,column=1,sticky=tk.W+tk.E)
                
        self.display_Frame.pack()'''
        
        self.display_Frame1 = tk.Frame(self.windowManager)
        self.display_Frame1.columnconfigure(0, weight=1)
        self.display_Frame1.columnconfigure(1, weight=1)
        self.display_Frame1.columnconfigure(2, weight=1)
        
        self.headingItemDescription = tk.Label(self.display_Frame1, text="Invoice Number", border=2)
        self.headingItemDescription.grid(row=0,column=0,sticky=tk.W+tk.E)
        
        self.headingPrice = tk.Label(self.display_Frame1, text="Tracking Number", border=2)
        self.headingPrice.grid(row=0,column=1,sticky=tk.W+tk.E)
                
        self.headingQty = tk.Label(self.display_Frame1, text="Location", border=2)
        self.headingQty.grid(row=0,column=2,sticky=tk.W+tk.E)
        
        for row_num, row in enumerate(self.result):
            #print(row_num, row)
            for col_num, col in enumerate(row):
                print(f"({row_num}, {col_num}) -> {col}")
                                
                self.data = tk.Label(self.display_Frame1, text=col)
                self.data.grid(row=row_num+1,column=col_num,sticky=tk.W+tk.E)
        
        self.display_Frame1.pack()

    def reps(self):
        messagebox.showerror("Report Generating Error", "Unable to Generate Report at the moment")

    
    '''def trackingSearch(self):
        self.search = self.searchEntry.get()
        try: 
            self.cursor = dbAccess.cursor()
            self.cursor.execute("SELECT * FROM sales WHERE `tracking_num` = %s", (self.search))
            self.result1 = self.cursor.fetchone()
        except mysql.connector.Error as e:
            print(f"An error occurred: {e}")
        finally:
            for row_num, row in enumerate(self.result):
                print(row_num, row)
                #for col_num, col in enumerate(row):
                    #print(f"({row_num}, {col_num}) -> {col}")
                    
                #self.data = tk.Label(self.display_Frame, text=row)
                #self.data.grid(row=,column=row_num,sticky=tk.W+tk.E)
            
        self.display_Frame1.pack()'''

'''class Tracking:
    
    def __init__(self):
        self.windowManager = tk.Tk()

        self.windowManager.geometry("100x100")
        self.windowManager.title("Tracking")
        
        
        
        self.windowManager.mainloop()
    '''        

class PurchasesView:
    
    def __init__(self):
        self.windowManager = tk.Tk()

        self.windowManager.geometry("900x500")
        self.windowManager.title("Test")
        
        self.menuLayout()
        
        self.displayScreen()
        
        self.windowManager.mainloop()
        
    def logOut(self):
        self.windowManager.destroy()
        LogIn()
    
    def gotoInventory(self):
        self.windowManager.destroy()
        InventoryView()
    
    def gotoReports(self):
        self.windowManager.destroy()
        ReportsView()
    
    def gotoOrderTracking(self):
        self.windowManager.destroy()
        OrderTrackingView()
    
    def gotoPurchases(self):
        self.windowManager.destroy()
        PurchasesView()
    
    def gotoInventoryUpdate(self):
        self.windowManager.destroy()
        InventoryUpdateView()
    
    def gotoAddItem(self):
        self.windowManager.destroy()
        AddItemView()

    def home(self):
        self.windowManager.destroy()
        ManagerSub()
        
    def menuLayout(self):
        self.menuBar = tk.Menu(self.windowManager)
        self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
        self.reportMenu = tk.Menu(self.menuBar, tearoff=0)
        self.inventoryMenu =tk.Menu(self.menuBar, tearoff=0)
        self.salesMenu = tk.Menu(self.menuBar, tearoff=0)
        self.reportGen = tk.Menu(self.menuBar, tearoff=0)
        
        self.menuBar.add_cascade(menu=self.fileMenu, label="File")
        self.menuBar.add_cascade(menu=self.reportMenu, label="Report")
        self.menuBar.add_cascade(menu=self.inventoryMenu, label="Inventory")
        self.menuBar.add_cascade(menu=self.salesMenu, label="Sales")
        
        self.fileMenu.add_command(label="LogOut", command=self.logOut)
        self.fileMenu.add_command(label="Dashboard", command=self.home)
        
        self.reportMenu.add_cascade(label="Generate Report", menu=self.reportGen, command=self.gotoReports)
        self.reportGen.add_command(label="Monthly Sales Report", command=self.reps)
        self.reportGen.add_command(label="Annual Sales Report", command=self.reps)
        self.reportGen.add_command(label="Inventory Report", command=self.reps)
        self.reportGen.add_command(label="Customer Report", command=self.reps)
        
        self.inventoryMenu.add_command(label="Add Item", command=self.gotoAddItem)
        self.inventoryMenu.add_command(label="Update Stock", command=self.gotoInventoryUpdate)
        self.inventoryMenu.add_command(label="Review Stock", command=self.gotoInventory)
        
        self.salesMenu.add_command(label="Review Sale", command=self.gotoPurchases)
        self.salesMenu.add_separator()
        self.salesMenu.add_command(label="Track Order", command=self.gotoOrderTracking)
                
        self.windowManager.config(menu=self.menuBar)

    def displayScreen(self):
        
        self.cursor = dbAccess.cursor()
        self.cursor.execute("SELECT `invoice_num`, `customer_id`, `price` FROM sales where `sales`.`refunded` = 0")
        self.result = self.cursor.fetchall()
        
        '''self.display_Frame = tk.Frame(self.windowManager)
        self.display_Frame.columnconfigure(0, weight=1)
        self.display_Frame.columnconfigure(1, weight=1)
        
        self.searchEntry = tk.Entry(self.display_Frame,)
        self.searchEntry.grid(row=0,column=0,sticky=tk.W+tk.E)
        
        self.searchBtn = tk.Button(self.display_Frame,text="Search", command=exit, border=1)
        self.searchBtn.grid(row=0,column=1,sticky=tk.W+tk.E)
                
        self.display_Frame.pack()'''
        
        self.display_Frame1 = tk.Frame(self.windowManager)
        self.display_Frame1.columnconfigure(0, weight=1)
        self.display_Frame1.columnconfigure(1, weight=1)
        self.display_Frame1.columnconfigure(2, weight=1)
        self.display_Frame1.columnconfigure(3, weight=1)
        
        self.headingItemDescription = tk.Label(self.display_Frame1, text="Invoice Number", border=2)
        self.headingItemDescription.grid(row=0,column=0,sticky=tk.W+tk.E)
        
        self.headingPrice = tk.Label(self.display_Frame1, text="Customer", border=2)
        self.headingPrice.grid(row=0,column=1,sticky=tk.W+tk.E)
                
        self.headingQty = tk.Label(self.display_Frame1, text="Price", border=2)
        self.headingQty.grid(row=0,column=2,sticky=tk.W+tk.E)
        
        for row_num, row in enumerate(self.result):
            print(row_num, row)
            for col_num, col in enumerate(row):
                print(f"({row_num}, {col_num}) -> {col}")
                
                if col_num == 2:
                    self.dataBtn = tk.Button(self.display_Frame1, text="Refund", command=self.refund)
                    self.dataBtn.grid(row=row_num+1,column=col_num+1,sticky=tk.W+tk.E)
                    self.data = tk.Label(self.display_Frame1, text=col)
                    self.data.grid(row=row_num+1,column=col_num,sticky=tk.W+tk.E)
                else: 
                    self.data = tk.Label(self.display_Frame1, text=col)
                    self.data.grid(row=row_num+1,column=col_num,sticky=tk.W+tk.E)
                
                '''self.data = tk.Label(self.display_Frame1, text=col)
                self.data.grid(row=row_num+1,column=col_num,sticky=tk.W+tk.E)'''
        
        self.display_Frame1.pack()

    def reps(self):
        messagebox.showerror("Report Generating Error", "Unable to Generate Report at the moment")

    def refund(self):
        
        self.cursor = dbAccess.cursor()
        self.cursor.execute("UPDATE `sales` SET `refunded` = '1' WHERE `sales`.`sales_id` = 2")
        dbAccess.commit()
        
        messagebox.showinfo("Refund Message", "Successful Refund")
        
        self.gotoPurchases()

class InventoryUpdateView:
    
    def __init__(self):
        self.windowManager = tk.Tk()

        self.windowManager.geometry("900x500")
        self.windowManager.title("Test")
        
        self.menuLayout()
        
        self.displayScreen()
        
        self.windowManager.mainloop()
        
    def logOut(self):
        self.windowManager.destroy()
        LogIn()
    
    def gotoInventory(self):
        self.windowManager.destroy()
        InventoryView()
    
    def gotoReports(self):
        self.windowManager.destroy()
        ReportsView()
    
    def gotoOrderTracking(self):
        self.windowManager.destroy()
        OrderTrackingView()
    
    def gotoPurchases(self):
        self.windowManager.destroy()
        PurchasesView()
    
    def gotoInventoryUpdate(self):
        self.windowManager.destroy()
        InventoryUpdateView()
    
    def gotoAddItem(self):
        self.windowManager.destroy()
        AddItemView()

    def home(self):
        self.windowManager.destroy()
        ManagerSub()
        
    def menuLayout(self):
        self.menuBar = tk.Menu(self.windowManager)
        self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
        self.reportMenu = tk.Menu(self.menuBar, tearoff=0)
        self.inventoryMenu =tk.Menu(self.menuBar, tearoff=0)
        self.salesMenu = tk.Menu(self.menuBar, tearoff=0)
        self.reportGen = tk.Menu(self.menuBar, tearoff=0)
        
        self.menuBar.add_cascade(menu=self.fileMenu, label="File")
        self.menuBar.add_cascade(menu=self.reportMenu, label="Report")
        self.menuBar.add_cascade(menu=self.inventoryMenu, label="Inventory")
        self.menuBar.add_cascade(menu=self.salesMenu, label="Sales")
        
        self.fileMenu.add_command(label="LogOut", command=self.logOut)
        self.fileMenu.add_command(label="Dashboard", command=self.home)
        
        self.reportMenu.add_cascade(label="Generate Report", menu=self.reportGen, command=self.gotoReports)
        self.reportGen.add_command(label="Monthly Sales Report", command=self.reps)
        self.reportGen.add_command(label="Annual Sales Report", command=self.reps)
        self.reportGen.add_command(label="Inventory Report", command=self.reps)
        self.reportGen.add_command(label="Customer Report", command=self.reps)
        
        self.inventoryMenu.add_command(label="Add Item", command=self.gotoAddItem)
        self.inventoryMenu.add_command(label="Update Stock", command=self.gotoInventoryUpdate)
        self.inventoryMenu.add_command(label="Review Stock", command=self.gotoInventory)
        
        self.salesMenu.add_command(label="Review Sale", command=self.gotoPurchases)
        self.salesMenu.add_separator()
        self.salesMenu.add_command(label="Track Order", command=self.gotoOrderTracking)
                
        self.windowManager.config(menu=self.menuBar)

    def displayScreen(self):
        
        self.item = 1001
        self.data = []
        
        self.cursor = dbAccess.cursor()
        self.cursor.execute("SELECT * FROM inventory where id = %s", (self.item,))
        self.result = self.cursor.fetchone()
        
        for row_num, row in enumerate(self.result):
            print(row_num, row)
            self.data.append(row)
            '''for col_num, col in enumerate(row):
                print(f"({row_num}, {col_num}) -> {col}")'''
        
        print(self.data[1])
                
        self.itemNameLabel = tk.Label(self.windowManager, text=("Item Name: "))
        self.itemNameLabel.place(x=20,y=10)
        self.itemNameEntry = tk.Entry(self.windowManager)
        self.itemNameEntry.insert(0,self.data[1])
        self.itemNameEntry.place(x=100,y=10)
        
        self.itemCodeLabel = tk.Label(self.windowManager, text="Item Code: ")
        self.itemCodeLabel.place(x=320,y=10)
        self.itemCodeEntry = tk.Entry(self.windowManager)
        self.itemCodeEntry.insert(0,self.data[2])
        self.itemCodeEntry.place(x=400,y=10)
        
        self.priceLabel = tk.Label(self.windowManager, text="Price: ")
        self.priceLabel.place(x=20,y=40)
        self.priceEntry = tk.Entry(self.windowManager)
        self.priceEntry.insert(0,self.data[3])
        self.priceEntry.place(x=100,y=40)
        
        self.qtyOnHandLabel = tk.Label(self.windowManager, text="Quantity: ")
        self.qtyOnHandLabel.place(x=320,y=40)
        self.qtyOnHandEntry = tk.Entry(self.windowManager)
        self.qtyOnHandEntry.insert(0,self.data[4])
        self.qtyOnHandEntry.place(x=400,y=40)
        
        self.descriptionLabel = tk.Label(self.windowManager, text="Description: ")
        self.descriptionLabel.place(x=20,y=70)
        self.descriptionTextField = tk.Text(self.windowManager,wrap="word",height=10,width=45)
        self.descriptionTextField.insert(tk.END,self.data[5])
        self.descriptionTextField.place(x=100,y=70)
        
        self.submitBtn = tk.Button(self.windowManager, text="Save", command=self.save)
        self.submitBtn.place(x=490,y=210)

    def reps(self):
        messagebox.showerror("Report Generating Error", "Unable to Generate Report at the moment")

    def save(self):
        self.itemName = self.itemNameEntry.get()
        self.itemCode = self.itemCodeEntry.get()
        self.price = self.priceEntry.get()
        self.qtyOnHand = self.qtyOnHandEntry.get()
        self.description = self.descriptionTextField.get("1.0",tk.END)
        
        self.cursor = dbAccess.cursor()
        self.cursor.execute("UPDATE `inventory` SET `item_name` = %s, `item_code` = %s, `price` = %s, `qty_on_hand` = %s, `descpri` = %s WHERE `inventory`.`id` = %s", (self.itemName,self.itemCode,self.price,self.qtyOnHand,self.description,self.data[0]))
        dbAccess.commit()
        
        messagebox.showinfo("Save", "Product Saved")
                
        print(f"Item Name: {self.itemName} \t Item Code: {self.itemCode} \nItem Price: {self.price} \t Item Quantity: {self.qtyOnHand} \nItem description: {self.description} \n ")
        
        print(self.data)
        
        self.gotoInventory()

class AddItemView:
    
    def __init__(self):
        self.windowManager = tk.Tk()

        self.windowManager.geometry("900x500")
        self.windowManager.title("Test")
        
        self.menuLayout()
        
        self.displayScreen()
        
        self.windowManager.mainloop()
        
    def logOut(self):
        self.windowManager.destroy()
        LogIn()
    
    def gotoInventory(self):
        self.windowManager.destroy()
        InventoryView()
    
    def gotoReports(self):
        self.windowManager.destroy()
        ReportsView()
    
    def gotoOrderTracking(self):
        self.windowManager.destroy()
        OrderTrackingView()
    
    def gotoPurchases(self):
        self.windowManager.destroy()
        PurchasesView()
    
    def gotoInventoryUpdate(self):
        self.windowManager.destroy()
        InventoryUpdateView()
    
    def gotoAddItem(self):
        self.windowManager.destroy()
        AddItemView()

    def home(self):
        self.windowManager.destroy()
        ManagerSub()

    def menuLayout(self):
        self.menuBar = tk.Menu(self.windowManager)
        self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
        self.reportMenu = tk.Menu(self.menuBar, tearoff=0)
        self.inventoryMenu =tk.Menu(self.menuBar, tearoff=0)
        self.salesMenu = tk.Menu(self.menuBar, tearoff=0)
        self.reportGen = tk.Menu(self.menuBar, tearoff=0)
        
        self.menuBar.add_cascade(menu=self.fileMenu, label="File")
        self.menuBar.add_cascade(menu=self.reportMenu, label="Report")
        self.menuBar.add_cascade(menu=self.inventoryMenu, label="Inventory")
        self.menuBar.add_cascade(menu=self.salesMenu, label="Sales")
        
        self.fileMenu.add_command(label="LogOut", command=self.logOut)
        self.fileMenu.add_command(label="Dashboard", command=self.home)
        
        self.reportMenu.add_cascade(label="Generate Report", menu=self.reportGen, command=self.gotoReports)
        self.reportGen.add_command(label="Monthly Sales Report", command=self.reps)
        self.reportGen.add_command(label="Annual Sales Report", command=self.reps)
        self.reportGen.add_command(label="Inventory Report", command=self.reps)
        self.reportGen.add_command(label="Customer Report", command=self.reps)
        
        self.inventoryMenu.add_command(label="Add Item", command=self.gotoAddItem)
        self.inventoryMenu.add_command(label="Update Stock", command=self.gotoInventoryUpdate)
        self.inventoryMenu.add_command(label="Review Stock", command=self.gotoInventory)
        
        self.salesMenu.add_command(label="Review Sale", command=self.gotoPurchases)
        self.salesMenu.add_separator()
        self.salesMenu.add_command(label="Track Order", command=self.gotoOrderTracking)
                
        self.windowManager.config(menu=self.menuBar)
        
    def displayScreen(self):
                
        self.itemNameLabel = tk.Label(self.windowManager, text=("Item Name: "))
        self.itemNameLabel.place(x=20,y=10)
        self.itemNameEntry = tk.Entry(self.windowManager)
        self.itemNameEntry.place(x=100,y=10)
        
        self.itemCodeLabel = tk.Label(self.windowManager, text="Item Code: ")
        self.itemCodeLabel.place(x=320,y=10)
        self.itemCodeEntry = tk.Entry(self.windowManager)
        self.itemCodeEntry.place(x=400,y=10)
        
        self.priceLabel = tk.Label(self.windowManager, text="Price: ")
        self.priceLabel.place(x=20,y=40)
        self.priceEntry = tk.Entry(self.windowManager)
        self.priceEntry.place(x=100,y=40)
        
        self.qtyOnHandLabel = tk.Label(self.windowManager, text="Quantity: ")
        self.qtyOnHandLabel.place(x=320,y=40)
        self.qtyOnHandEntry = tk.Entry(self.windowManager)
        self.qtyOnHandEntry.place(x=400,y=40)
        
        self.descriptionLabel = tk.Label(self.windowManager, text="Description: ")
        self.descriptionLabel.place(x=20,y=70)
        self.descriptionTextField = tk.Text(self.windowManager,wrap="word",height=10,width=45)
        self.descriptionTextField.place(x=100,y=70)
        
        self.submitBtn = tk.Button(self.windowManager, text="Save", command=self.save)
        self.submitBtn.place(x=490,y=210)

    def reps(self):
        messagebox.showerror("Report Generating Error", "Unable to Generate Report at the moment")

    def save(self):
        self.itemName = self.itemNameEntry.get()
        self.itemCode = self.itemCodeEntry.get()
        self.price = self.priceEntry.get()
        self.qtyOnHand = self.qtyOnHandEntry.get()
        self.description = self.descriptionTextField.get("1.0",tk.END)
        
        self.cursor = dbAccess.cursor()
        self.cursor.execute("INSERT INTO `inventory` (`id`, `item_name`, `item_code`, `price`, `qty_on_hand`, `descpri`) VALUES (NULL, %s, %s, %s, %s, %s)", (self.itemName,self.itemCode,self.price,self.qtyOnHand,self.description))
        dbAccess.commit()
        
        messagebox.showinfo("Save", "Product Saved")
                
        print(f"Item Name: {self.itemName} \t Item Code: {self.itemCode} \nItem Price: {self.price} \t Item Quantity: {self.qtyOnHand} \nItem description: {self.description} \n ")
        
        #print(self.data)
        
        self.itemNameEntry.delete(0,tk.END)
        self.itemCodeEntry.delete(0,tk.END)
        self.priceEntry.delete(0,tk.END)
        self.qtyOnHandEntry.delete(0,tk.END)
        self.descriptionTextField.delete("1.0",tk.END)
        
        
LogIn()

#InventoryUpdateView()

#InventoryView()

#ManagerSub()

#ReportsView()