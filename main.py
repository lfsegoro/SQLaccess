import tkinter as tk
#from tkinter import Label, Entry, Button, Tk
from time import sleep
from mysql_connector import *
from query import *
import sys
import time

#  Global variable, function
#  ========================================================================================
username_status = "not ok"
password_status = "not ok"

#  START Function definiton for username and password
#  ==============================================================================
def check_username():
    FrameWidgetC.frame_obj['20'].offdisplay()
    FrameWidgetC.frame_obj['10'].offdisplay()
    username = EntryWidget.ent_obj['000100'].get_by_expression()
    print("check_username called: ", username)
    global username_status
    obj = ""
    if username != "":
        obj = SelectSqlObj('radcheck', 'username', 'username', username).select()  # call mysql to check exist or not
        for i in range(2, 0, -1):
            sys.stdout.write(str(i) + ' ')
            sys.stdout.flush()
            time.sleep(1)
        print("\n")
        try:
            LabelWidget.label_obj['000200'].deconstruct('000200')
        except:
            pass #print('the object not exist yet')
        finally:
            if len(obj) > 0:
                LabelWidget('00', 2, 0, 'User Exist!!→→→ ', 'blue')
                username_status = "not ok"
                FrameWidgetC.frame_obj['20'].ondisplay()
                FrameWidgetC.frame_obj['10'].ondisplay()
                tbl_userinfo(username)
            else:
                username_status = "ok"
                FrameWidgetC.frame_obj['20'].offdisplay()
                FrameWidgetC.frame_obj['10'].offdisplay()
    else:
        LabelWidget('00', 2, 0, 'Username can\'t Empty!! ', '#f00')
        FrameWidgetC.frame_obj['20'].offdisplay()
        FrameWidgetC.frame_obj['10'].offdisplay()
        username_status = "not ok"
    print(username_status, password_status)
    return username
def check_password():
    password = EntryWidget.ent_obj['000101'].get_by_expression()
    print("check_password called :", password)
    global password_status
    try:
        LabelWidget.label_obj['000201'].deconstruct('000201')
    except:
        pass # print('obj above not created yet')
    finally:
        if password == "":
            if '000200' not in LabelWidget.label_obj:
                LabelWidget('00', 2, 1, 'Password can\'t Empty', '#f00')
            password_status = "not ok"
            #return
        else:
            password_status = "ok"
    print("username: " , username_status, "password: " , password_status)
    return password
def insert_to_table(table_name, username):  # general purpose function
    InserSqlObj(table_name, 'username', username).insert()
#  ==============================================================================
#  END of Global variables, function
#  START userinfo function
#  ==============================================================================
def tbl_structure(sql='describe userinfo'): # general purpose function
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    result_list = [list(row) for row in rows]
    return result_list

# def primarysql(table_name, sql=None):
#     sql = SELECT COLUMN_NAME FROM information_schema.KEY_COLUMN_USAGE WHERE TABLE_NAME = 'wimax' AND CONSTRAINT_NAME = 'PRIMARY'
#
#     tbl_structure(sql)
#
# def isemptytbl(table_name, sql=None):
#     sql = ???
#     a = tbl_structure(sql)
#     if a:
#         return False
#     else:
#         return True
def tbl_query(username):  # general purpose function
    list_of_list = SelectSqlObj( 'userinfo', '*', 'username', username).select_n_convert()
    tabl = list_of_list[0]
    return tabl
def tbl_userinfo(username):  # specific func for userinfo
    global username_status
    global password_status
    username_status = "not ok"
    password_status = "not ok"
    userinfo = tbl_query(username)
    userinfo_struct = tbl_structure('describe userinfo')
    LabelWidget('10', 2, 3, "U S E R I N F O")
    LabelWidget('20', 2, 0, "<==============")
    LabelWidget('10', 2, 4, "===============>")
    LabelWidget('20', 2, 1, "Klik id area to \n cancel change")
    for i in range(len(userinfo)):
        LabelWidget('20', 0, i, userinfo_struct[i][0])
        if i == 1 or i == 0:
            EntryWidget('20', 1, i, str(userinfo[i]), 'blue', 'readonly')
        else:
            EntryWidget('20', 1, i).method_3(str(userinfo[i]))
    ButtonUserinfo('20', 1, i+1, '^Submit Update^')
    EntryWidget.ent_obj['200100'].bind_outside()


def sql_gnrl(sql):
    print(sql)
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    # print(rows)
    result_list = [list(row) for row in rows]
    # print(result_list)
    return result_list

def def_level(val):
    result, level = [], 'root'
    try:
        result = sql_gnrl('show ' + val)
        if result:
            return result, level
    except:
        result = sql_gnrl('describe ' + val)
        if result:
            level = 'table'
            return result, level
        else:
            level = 'entry'
            return result, level


def iterate_newidget(result, frameid, column, val, level):
    # print('checked2 ')
    pairs = {}
    stack = len(result)
    #print(len(result))
    for i in range(stack):
        # print(result[i][0], end="\n")
        val = result[i][0]

        if i < 20:

            # LabelWidget(frameid, column, i + row, val + ":")
            LabelWidget(frameid, column, i , val + ":")

            key = frameid + (str(column)).zfill(2) + (str(i)).zfill(2)

            pairs[key] = val
            print("checked i = ", i, frameid, val, key)
            if level in ['root', 'tables'] :

                LabelWidget.label_obj[key].binded(frameid, column, i, val)

        else:
            row=i
            LabelWidget(frameid, column+2, i - 20, val + ":")

            key = frameid + (str(column+2)).zfill(2) + (str(i - 20)).zfill(2)

            pairs[key] = val
            if level in ['root', 'tables'] :
                LabelWidget.label_obj[key].binded(frameid, column, i-20, val)
            print("checked i = ", i, frameid, val, key)

    return len(result)

root = tk.Tk()
root.title('SQLTk')
#root.geometry('600x400')
class FrameWidgetC(tk.Frame):
    frame_obj = {}
    def __init__(self, parent, frameid, sticky=None,  bg=None,):
        tk.Frame.__init__(self, parent, bg=bg)
        column=frameid[:1]
        row=frameid[1:]
        self.id = str(column) + str(row)
        # label2 = tk.Label(self, text = "|----------------------------------------------------|")
        # label2.grid(column=0, row=0)
        # label1 = tk.Label(self, text = self.id )
        # label1.grid(column=0, row=2)
        # button1 = tk.Button(self, text = "Do Something")
        # button1.grid()
        # button1.bind("<Button-1>", self.method1)
        # button1.bind("<Button-2>", self.method2)
        self.grid(column=column, row=row, sticky=sticky, )
        # self.grid_propagate(prop)
        FrameWidgetC.frame_obj[self.id] = self

    def method1(self, event):
        self.destroy()
        # self.grid_remove()
    def method2(self, event):
        txt = input("Enter id ")
        LabelWidget.label_obj[str(txt)].method1()

    def offdisplay(self):
        self.grid_remove()
    def ondisplay(self):
        self.grid()

class LabelWidget:
    label_obj = {}
    def __init__(self, frameid, column, row, text, fg='black'):
        self.id = frameid + (str(column)).zfill(2) + (str(row)).zfill(2)
        print(self.id)
        self.label = tk.Label(FrameWidgetC.frame_obj[frameid], text = text, fg=fg, cursor='hand1')
        self.label.grid(column=column, row=row)
        LabelWidget.label_obj[self.id] = self
        self.label.bind("<Expose>", self.visibilityChanged)
    def visibilityChanged(self, event):
        print('i am obstructed ', self.id)
    def deconstruct(self, key):
        self.label.destroy()
        LabelWidget.label_obj.pop(key)
    def binded(self, frameid, column, row, val):
        #frameid= str(int(frameid[:1])+1) + frameid[1:]
        #print(frameid)
        self.label.bind("<Button-3>", lambda event, frameid=frameid, column=column,
                         row=row, val=val: self.special_l(frameid,
                         column, row, val ))

    def special_l(self, frameid, column, row, val):  # define each dynamic widget to each event
        print('event detected in function special_l for:', val)
        result, level = def_level(val)
        print(result)
        print(level, frameid)
        shift = 0
        match level:
         case 'root':
            shift = 1
            print("del me1  ", frameid, val)
            frameid = str(int(frameid[:1])+shift) + frameid[1:]
            for widget in FrameWidgetC.frame_obj[frameid].winfo_children():
                  widget.destroy()
            iterate_newidget(result, frameid, column, val, level)
            print('checked4', frameid, column, row, val)

         case 'table':
            shift = 1
            frameid = str(int(frameid[:1]) + shift) + frameid[1:]
            print("del me2 :", frameid, val)
            for widget in FrameWidgetC.frame_obj[frameid].winfo_children():
                 widget.destroy()
            for widget in FrameWidgetC.frame_obj[str(int(frameid[:1]) + shift) + frameid[1:]].winfo_children():
                 widget.destroy()
            print("del me2 :", frameid, val)

            lenght = iterate_newidget(result, frameid, column, val, level)
            print(lenght)
            # for widget in FrameWidgetC.frame_obj['30'].winfo_children():
            #     widget.destroy()
            for i in range(lenght):
                #EntryWidget(frameid, column+1, i)
                if i < 20:
                    EntryWidget(frameid, column + 1, i)
                else:
                    EntryWidget(frameid, column + 3, i-20)


class EntryWidget:
    ent_obj = {}
    def __init__(self, frameid, column, row, text='', fg='black', state='normal'):
        self.v = tk.StringVar()
        self.v.set(text)
        self.id = frameid + (str(column)).zfill(2) + (str(row)).zfill(2)  # a unique identifier for the object/widget
        # if self.id != '2010':
        if 1==1:
            self.entry = tk.Entry(FrameWidgetC.frame_obj[frameid], textvariable=self.v, state=state, fg=fg)
            self.entry.grid(column=column, row=row)
            self.entry.bind("<KeyRelease>", self.method)
        else:
            pass
        EntryWidget.ent_obj[self.id] = self

    def method(self, event):
        self.entry.get()
    def get_by_expression(self):
        return self.entry.get()
    def method_3(self, txt):  # will remove this later, already have textvariable in init.
        self.entry.insert(0, txt)
    def bind_outside(self):
        self.entry.bind("<Button-1>", self.special)
    def special(self, e):
        tbl_userinfo(EntryWidget.ent_obj['000100'].get_by_expression())
        print("result of chain reaction")
    def destruct(self):
        self.entry.destroy()
class ButtonWidget:
    btn_obj = {}
    def __init__(self, frameid, column, row, text='default'):
        self.button = tk.Button(FrameWidgetC.frame_obj[frameid], text=text)
        self.id = frameid + (str(column)).zfill(2) + (str(row)).zfill(2)
        self.button.grid(column=column, row=row)
        self.button.bind("<Button-1>", self.method)
        ButtonWidget.btn_obj[self.id] = self

    def method(self, event):
        if "000200" in LabelWidget.label_obj:
            print("user exist")
        else:
            print("user available")
        for widget in FrameWidgetC.frame_obj['20'].winfo_children():
            widget.destroy()
        for widget in FrameWidgetC.frame_obj['10'].winfo_children():
            widget.destroy()
        username = check_username()  # inside this func there is branch to the End of Routine
        password = check_password()
        if password_status == 'ok' and username_status == "ok":
            LabelWidget('00', 2, 0, 'Username Created', 'green')
            InserSqlObj('radcheck', 'username, value', username + "\' , \'"
                        + password).insert()  # <<create username
            InserSqlObj('userinfo', 'username', username).insert()  # <<create userinfo
            FrameWidgetC.frame_obj['20'].ondisplay()
            FrameWidgetC.frame_obj['10'].ondisplay()
            tbl_userinfo(username)
class ButtonUserinfo(ButtonWidget):
    def __init__(self, frameid, column, row, text='default'):
        super().__init__(frameid, column, row, text)
        self.button.bind("<Button-1>", self.method)
    def method(self, event):
        username = EntryWidget.ent_obj['200101'].get_by_expression()
        userinfo = tbl_query(username)
        userinfo_struct = tbl_structure()
        print(userinfo_struct, "\n", "\n", "\n", )
        for i in range(2, len(userinfo)):
            try:  # to skip if errors occur in iterations
                UpdateSqlTbl("userinfo", userinfo_struct[i][0], username,
                             EntryWidget.ent_obj["2001" + (str(i)).zfill(2)].get_by_expression()).update()
            except:
                print('skipped ?')
            finally:
                print('end')

FrameWidgetC(root, '00',  "nw")
# FrameWidgetC(root, '10' ,"n"); FrameWidgetC(root, '20', "n")
# FrameWidgetC(root, '30', 'yellow', "n")
# FrameWidgetC(root, '01','lightgreen', "n" );FrameWidgetC(root, '02','lightgreen', "n" )

LabelWidget('00', 0, 0, "Username: "); EntryWidget('00', 1, 0, )
LabelWidget('00', 0, 1, "Password: "); EntryWidget('00', 1, 1, )
ButtonWidget('00', 1, 2, 'Check/Submit')  # all algorithm START HERE, and will loop back here.
# dynamic widget generating
frameid, column, row, val = '10', 0 ,0 , 'tables'
FrameWidgetC(root,frameid,'n')
FrameWidgetC(root, str(int(frameid[:1])+1) + frameid[1:], 'n')
FrameWidgetC(root, str(int(frameid[:1])+2) + frameid[1:], 'n')
FrameWidgetC(root, str(int(frameid[:1])+3) + frameid[1:], 'n')
FrameWidgetC(root, str(int(frameid[:1])+4) + frameid[1:], 'n')
LabelWidget.label_obj['000000'].binded(frameid,column,row,val)  # clue: right click on 'username' label widget
#print (str(int(frameid[:1])+1) + frameid[1:])
root.mainloop()