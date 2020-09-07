import psutil
import time
import tkinter as tk
import sqlite3
from sqlite3 import Error
import datetime 
import matplotlib.pyplot as plt

class Network:
    def __init__(self,master):
        # Label sent
        self.label=tk.Label(master)
        self.label.grid(row=0, column=0)
        self.label.configure(text='nothing')
        
        # Label recv
        self.label2 = tk.Label(master)
        self.label2.grid(row = 3,column = 0)
        self.label2.configure(text = 'nothing')
        self.button_value = 0
        self.count = 0
        
        # data type is for changing from byte to kilo to mega 
        self.data_type = pow(1000,2)
        self.st_sent = psutil.net_io_counters().bytes_sent 
        self.st_recv = psutil.net_io_counters().bytes_recv 
        self.current_recv = 0 
        self.current_sent = 0
        self.starting_time = datetime.datetime.now()
        self.current_time = datetime.datetime.now()
        self.selected_time = 0

        self.create_button(master) 
        self.update_label()
        # getting current date, this will be used for graph information later. 
  
    def update_current_time(self):
        # updates the current time 
        self.current_time = datetime.datetime.now()
        
    def change_type(self):
        # changes the tpye of data value. 
        print("change tpye")
        self.button_value += 1
        if self.button_value >= 3:
            self.button_value = 0
        if self.button_value == 0:
            self.button.configure(text = 'Byte')
            self.data_type = 1
        if self.button_value == 1:
            self.button.configure(text = 'Kilo')
            self.data_type = 1024
        if self.button_value == 2:
            self.button.configure(text = 'Mega')
            self.data_type = 1024*1024
    
    def update_label(self):
            # Updates the labels information with the most current information and logs it
            self.current_sent = psutil.net_io_counters().bytes_sent / self.data_type - (self.st_sent / self.data_type)
            self.current_recv = psutil.net_io_counters().bytes_recv / self.data_type - (self.st_recv / self.data_type)
            self.label.configure(text = 'Current Total Received: {}'.format(self.current_recv))
            self.label2.configure(text = 'Current Total Sent: {}'.format(self.current_sent))

            self.update_current_time()
            data = (self.starting_time,self.current_time,psutil.net_io_counters().bytes_sent - self.st_sent ,psutil.net_io_counters().bytes_recv - (self.st_recv))
            self.inset_data(data)
            self.label.after(5000, self.update_label) # call this method again in 1,000 milliseconds

    def create_graph_ct(self):
        # creates a graph using the current time
        # first it creats a string for the sql statement then it will extract the information from the db. 
        # going to create a 2 line line graph. 
        
        conn = self.test_connection()
        cur = conn.cursor()
        # create a modified vesion of current time variable
        ct_value  = "'"+ str(self.starting_time) +"'"
        print(ct_value)
        sql = "SELECT * from project WHERE time_started = " + ct_value 
        cur.execute(sql)
        rows = cur.fetchall()
        recv_x = []
        sent_x = []
        time_y = []
        i = 0
        for row in rows:
            recv_x.append((row[4] / 1024)/1024)
            sent_x.append((row[3] / 1024)/1024)
            time_y.append(i)
            i += 5
        fig = plt.figure()
        ax1 = fig.add_subplot(221)
        ax2 = fig.add_subplot(222)
        ax1.plot(time_y,recv_x)
        ax2.plot(sent_x)
        
        plt.show()

    def get_all_time(self,master):
        # gets all the times from the database then creates a listbox to select them from. 
        conn = self.test_connection()
        cur = conn.cursor()
        sql = "SELECT time_started from project"
        cur.execute(sql)
        rows = cur.fetchall()
        
        # adds all the times that it fetched to a list. 
        time_list = []
        for row in rows:
            if row not in time_list:
                time_list.append(row)
        # Listbox and listbox's button. 
        var1 = tk.StringVar()
        lb = tk.Listbox(master,listvariable = var1,width = 30)
        for item in time_list:
            lb.insert('end',item)
        lb.grid(row = 9,column = 5)
        # command used to get the selected item from the list box. 
        def create_compatison_graph():
            value = lb.get(lb.curselection())   
            self.selected_time = str(value)
            replacement_list = ["'","(",")",","]
            
            for elements in replacement_list:
                self.selected_time = self.selected_time.replace(elements,'')
            print(self.selected_time)
            print(self.starting_time)
            # creates a graph using the current time
            # first it creats a string for the sql statement then it will extract the information from the db. 
            # going to create a 2 line line graph. 
            
            conn = self.test_connection()
            cur = conn.cursor()
            # create a modified vesion of current time variable
            ct_value  = "'"+ str(self.starting_time) +"'"
            sql = "SELECT * from project WHERE time_started = " + ct_value 
            cur.execute(sql)
            rows = cur.fetchall()
            recv_x = []
            sent_x = []
            time_y = []
            i = 0
            for row in rows:
                recv_x.append((row[4] / 1024)/1024)
                sent_x.append((row[3] / 1024)/1024)
                time_y.append(i)
                i += 5
            fig = plt.figure()
            ax1 = fig.add_subplot(221)
            ax2 = fig.add_subplot(222)
            ax1.plot(time_y,recv_x)
            ax2.plot(sent_x)
            
            compare_time_str = "'"+ str(self.selected_time) +"'"
            compare_sql = "SELECT * from project WHERE time_started = " + compare_time_str
            cur.execute(compare_sql)
            rows=cur.fetchall()
            compare_recv_x = []
            compare_sent_x = []
            compare_time_y = []
            i = 0
            for row in rows:
                compare_recv_x.append((row[4] / 1024)/1024)
                compare_sent_x.append((row[3] / 1024)/1024)
                compare_time_y.append(i)
                i += 5
            ax3 = fig.add_subplot(223)
            ax4 = fig.add_subplot(224)
            ax3.plot(compare_time_y,compare_recv_x)
            ax4.plot(compare_sent_x)


            plt.show()

 
        selection_button = tk.Button(text = 'Select Time to Compare to ', command = create_compatison_graph)
        selection_button.grid(row = 9,column = 7)
        

    def create_button(self,master):
        # Creates a button to change the Data's type 
        self.button = tk.Button(master)
        self.button.grid(row = 3, column = 5)
        self.button.configure(text = 'Change Data Type', command = self.change_type )
        
        # button for getting all items from db 
        self.db_button = tk.Button(master)
        self.db_button.grid(row = 4, column = 5)
        self.db_button.configure(text = 'Get items from db', command = self.get_all )

        # button for creating a graph with current time. 
        self.ct_button = tk.Button(master)
        self.ct_button.grid(row = 5, column = 5)
        self.ct_button.configure(text = "Create Graph for : " + str(self.starting_time), command = self.create_graph_ct)

        # button for getting all times. 
        self.get_times = tk.Button(master)
        self.get_times.grid(row = 6,column = 5)
        self.get_times.configure(text = "Get all times" , command =  lambda:self.get_all_time(master))

    def test_connection(self):
        """ create a database connection to a SQLite Database """
        db_file = 'database.db'
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return conn

    def get_all(self):
        database = 'database.db'
        conn = self.test_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM project")
        rows = cur.fetchall()
        for row in rows:
            print(row)
    
    def inset_data(self, data):
        # temp information will not be used later. 
        sql = '''INSERT INTO project(time_started, time_recorded, amount_sent, amount_recv) VALUES (?,?,?,?)'''
        conn = self.test_connection()
        cur = conn.cursor()
        cur.execute(sql,data)
        conn.commit()
        return cur.lastrowid

net = tk.Tk()
Network(net)
#Network(net).get_all()
net.mainloop()