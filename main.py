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
    username = EntryWidget.ent_obj['0010'].get_by_expression()
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
        # sleep(2)
        try:
            LabelWidget.label_obj['0020'].deconstruct('0020')
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
    password = EntryWidget.ent_obj['0011'].get_by_expression()
    print("check_password called :", password)
    global password_status
    try:
        LabelWidget.label_obj['0021'].deconstruct('0021')
    except:
        pass # print('obj above not created yet')
    finally:
        if password == "":
            if '0020' not in LabelWidget.label_obj:
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
    EntryWidget.ent_obj['2010'].bind_outside()


#  ========================================================================================
#  END userinfo function
# def center_window(width=300, height=200):
#     # get screen width and height
#     screen_width = root.winfo_screenwidth()
#     screen_height = root.winfo_screenheight()
#     # calculate position x and y coordinates
#     x = (screen_width/2) - (width/2)
#     y = (screen_height/2.3) - (height/2)
#     root.geometry('%dx%d+%d+%d' % (width, height, x, y))

root = tk.Tk()
root.title('Freeradius Database Management')
#center_window(600, 600)
#root.geometry('600x400')

class FrameWidgetC(tk.Frame):
    frame_obj = {}
    def __init__(self, parent, column, row, sticky=None):
        tk.Frame.__init__(self, parent)
        self.id = str(column) + str(row)
        # label2 = tk.Label(self, text = "|----------------------------------------------------|")
        # label2.grid(column=0, row=0)
        # label1 = tk.Label(self, text = self.id )
        # label1.grid(column=0, row=2)
        # button1 = tk.Button(self, text = "Do Something")
        # button1.grid()
        # button1.bind("<Button-1>", self.method1)
        # button1.bind("<Button-2>", self.method2)
        self.grid(column=column, row=row, sticky=sticky)
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


def special_l(sql):
    #print(sql)
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    result_list = [list(row) for row in rows]
    return result_list
def trytobegeneral(a, frameid, col_offset, row_offset, split, val):

    root_tbl = a
    pairs = {}
    stack = len(root_tbl) // split  # later will work to support split more than 2, currently only support split 1 or 2.
    for i in range(len(root_tbl)):
        # print(root_tbl[i][0], end="\n")
        val = root_tbl[i][0]
        if i < stack:
            LabelWidget(frameid, col_offset, i + row_offset, val + ":")
            key = frameid + str(col_offset) + str(i + row_offset)
            pairs[key] = val
            LabelWidget.label_obj[key].invokebind_gnrl(key, val, stack)
        else:
            LabelWidget(frameid, col_offset + split, i + row_offset - stack, val + ":")
            key = frameid + str(col_offset + split) + str(i + row_offset - stack)
            pairs[key] = val
            LabelWidget.label_obj[key].invokebind_gnrl(key, val, stack)
class LabelWidget:
    label_obj = {}

    def __init__(self, frameid, column, row, text, fg='black'):
        self.id = frameid + str(column) + str(row)
        # print(self.id)
        self.label = tk.Label(FrameWidgetC.frame_obj[frameid], text = text, fg=fg)
        self.label.grid(column=column, row=row)
        LabelWidget.label_obj[self.id] = self

    def deconstruct(self, key):
        self.label.destroy()
        LabelWidget.label_obj.pop(key)
    def invokebind(self, q):
        self.label.bind("<Button-1>", lambda q: exec("print('magic')"))
    def invokebind_gnrl(self, key, value, len):  # note: event not stated in parameter althoudh use by lambda
        self.label.bind("<Button-1>", lambda event, key=key, value=value, len=len
                         : self.method_gnrl(key, value, len))
    def method_gnrl(self, key, value, len):  # currently the container will be frame '01'
        #FrameWidgetC.frame_obj['20'].offdisplay()
        print(key," ", value)
        '''ready to work on pairs'''
        #a = tbl_structure('describe ' + value)
        # b = (a[1][0])
        a = self.special_l('30', 0, 0, 1, value)
        if a == 'dead end':
            print ('dead end on : ', key, value)
            for i in range(len):
                pass
        #inside_table_struct = ('describe' + value)
    def summon_other_widget(self, frameid, col_offset, row_offset, split, val=''):
        self.label.bind("<Button-3>", lambda event, frameid=frameid, col_offset=col_offset,
                         row_offset=row_offset, split=split: self.special_l(frameid,
                         col_offset, row_offset, split, val))

        #print(LabelWidget.label_obj)
    def special_l(self, frameid, col_offset, row_offset, split, val ):  # define each dynamic widget to each event
        a = []
        try:
            print("del me")
            sql = 'describe ' + val
            a = special_l(sql)
            print("try success ", a)
            b = True
        except:
            try:
                print("del me2  ", val)
                sql = 'show ' + val
                a = special_l(sql)
                print("exeption, try ng, ", a)
                b = True
            except:
                return 'dead end'

        if a:
            trytobegeneral(a, frameid, col_offset, row_offset, split, val)
        #
        # root_tbl = special_l(sql)
        # pairs = {}
        # stack = len(root_tbl)//split  # later will work to support split more than 2, currently only support split 1 or 2.
        # for i in range(len(root_tbl)):
        #     # print(root_tbl[i][0], end="\n")
        #     val = root_tbl[i][0]
        #     if i < stack:
        #         LabelWidget(frameid, col_offset, i+row_offset, val + ":")
        #         key = frameid + str(col_offset) + str(i+row_offset)
        #         pairs[key] = val
        #         LabelWidget.label_obj[key].invokebind_gnrl(key, val)
        #     else:
        #         LabelWidget(frameid, col_offset+split, i+row_offset-stack, val + ":")
        #         key = frameid + str(col_offset+split) + str(i+row_offset-stack)
        #         pairs[key] = val
        #         LabelWidget.label_obj[key].invokebind_gnrl(key, val)
        #print(LabelWidget.label_obj)


class ScrollBar:
    def __init__(self, column, row, columnspan='10', sticky=tk.NE):
        self.sb = tk.Scrollbar(root)
        self.sb.grid(column=column, row=row, columnspan=columnspan, sticky=sticky)
class EntryWidget:
    ent_obj = {}
    def __init__(self, frameid, column, row, text='', fg='black', state='normal'):
        self.v = tk.StringVar()
        self.v.set(text)
        self.id = frameid + str(column) + str(row)  # a unique identifier for the object/widget
        # if self.id != '2010':
        if 1==1:
            self.entry = tk.Entry(FrameWidgetC.frame_obj[frameid], textvariable=self.v, state=state, fg=fg)
            self.entry.grid(column=column, row=row)
            self.entry.bind("<KeyRelease>", self.method)
        else:
            pass
            # self.entry1 = tk.Entry(FrameWidgetC.frame_obj[frameid], textvariable=self.v, state=state, fg='red')
            # self.entry1.grid(column=column, row=row)
            # self.entry1.bind("<Button-1>", self.special)
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
        tbl_userinfo(EntryWidget.ent_obj['0010'].get_by_expression())
        print("result of chain reaction")
    def destruct(self):
        self.entry.destroy()


class ButtonWidget:
    def __init__(self, frameid, column, row, text='default'):
        self.button = tk.Button(FrameWidgetC.frame_obj[frameid], text=text)
        self.button.grid(column=column, row=row)
        self.button.bind("<Button-1>", self.method)
        self.button.bind("<Button-2>", self.method2)
        #self.button.bind("<Button-3>", self.method3)

    def method3(self, event):
        FrameWidgetC.frame_obj['20'].method3()
    def method2(self, event):
        EntryWidget.ent_obj['2010'].bind_outside()
    def method(self, event):
        if "0020" in LabelWidget.label_obj:
            print("user exist")
        else:
            print("user available")
        FrameWidgetC.frame_obj['20'].offdisplay()
        FrameWidgetC.frame_obj['10'].offdisplay()
        username = check_username()  # inside this func there is branch to the End of Routine
        password = check_password()
        if password_status == 'ok' and username_status == "ok":
            if '0020' in LabelWidget.label_obj:
                LabelWidget.label_obj['0020'].deconstruct('0020')
            if '0021' in LabelWidget.label_obj:
                LabelWidget.label_obj['0021'].deconstruct('0021')
            LabelWidget('00', 2, 0, 'Username Created', 'green')
            InserSqlObj('radcheck', 'username, value', username + "\' , \'"   # <<create username
                        + password).insert()
            InserSqlObj('userinfo', 'username', username).insert()  # <<create userinfo
            FrameWidgetC.frame_obj['20'].ondisplay()
            FrameWidgetC.frame_obj['10'].ondisplay()
            tbl_userinfo(username)

class ButtonUserinfo(ButtonWidget):
    def __init__(self, frameid, column, row, text='default'):
        super().__init__(frameid, column, row, text)
        self.button.bind("<Button-1>", self.method)
    def method(self, event):
        username = EntryWidget.ent_obj['2011'].get_by_expression()
        userinfo = tbl_query(username)
        userinfo_struct = tbl_structure()
        print(userinfo_struct, "\n", "\n", "\n", )
        for i in range(2, len(userinfo)):
            # UpdateSqlTbl("userinfo", userinfo_struct[i][0], username,
            #              EntryWidget.ent_obj["201" + str(i)].get_by_expression()).update()
        # if i<1:
            #print(userinfo_struct[i][0], ", " ,EntryWidget.ent_obj["201" + str(i)].method2())
            try:  # to skip if errors occur in iterations
                UpdateSqlTbl("userinfo", userinfo_struct[i][0], username,
                             EntryWidget.ent_obj["201" + str(i)].get_by_expression()).update()
            except:
                print('skipped ?')
            finally:
                print('end')

FrameWidgetC(root, 0, 0, 'nw') ;FrameWidgetC(root, 1, 0, 'n'); FrameWidgetC(root, 2, 0, 'n');FrameWidgetC(root, 3, 0, 'n')
FrameWidgetC(root, 0, 1)

LabelWidget('00', 0, 0, "Username: "); EntryWidget('00', 1, 0, )
LabelWidget('00', 0, 1, "Password: "); EntryWidget('00', 1, 1, )
ButtonWidget('00', 1, 2, 'Check/Submit')  # all algorithm START HERE, and will loop back here.
#print(LabelWidget.label_obj)
LabelWidget.label_obj['0000'].summon_other_widget('00', 0, 3, 2, 'tables')  # clue: right click on 'username' label widget
#print(LabelWidget.label_obj)

#ScrollBar(100,0)
# val = 'tables'
# try:
#     sql = 'describe ' + val
#     a = special_l(sql)
#     print("try success ", a)
# except:
#     sql = 'show ' + val
#     a = special_l(sql)
#     print("exeption, try ng, ", a)

root.mainloop()