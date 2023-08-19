from mysql_connector import *
def new_user(username, password):
    return ("insert into radcheck (username, value) values (" +
            "\'" + username + "\', " +
            "\'" + password + "\');")
def check_user(username):
    return ("select username from radcheck where username = " + "\'" + username + "\'")

def new_user_info(username):
    return ("insert into userinfo (username) values (" +
            "\'" + username + "\');")
def query_user_info(username):
    return ("select * from userinfo where username like " + "\'" + username + "\'")

#  START of query definition
#  ===================================================================================================



class UpdateSqlTbl:
    def __init__(self, table_name, column_name, field_anchor, field_var='j'):
        self.query = ("update " + table_name + " set " + column_name + " = " + "\'" + field_var + "\'" + " where username"
                      + " = " + "\'" + field_anchor + "\'"  )
        print(self.query)

    def update(self):  #  for select 1 item , best use for Describe Table_name
        mycursor.execute(self.query)
class SelectSqlObj:
    def __init__(self, table_name, column_name, field_anchor, field_var='j'):
        self.query = ("select " + column_name + " from " + table_name + " where "
                      + field_anchor + " = " + "\'" + field_var + "\'")
        query = (self.query)
        #mycursor.execute(self.query)


    def select(self):  #  for select 1 item , best use for Describe Table_name
        mycursor.execute(self.query)
        rows = mycursor.fetchall()
        list_of_list = [list(row) for row in rows]
        return list_of_list

    def select_n_convert(self):
        mycursor.execute(self.query)
        rows = mycursor.fetchall()
        list_of_list = [list(row) for row in rows]
        final = []
        for j in (range(len(list_of_list))):
            sf = []
            for i in list_of_list[j]:
                if i == None:
                    i = ""
                sf.append(i)
            final.append(sf)
        return final
def select_n_convert(query):  #  query = use real mysql syntak
    mycursor.execute(query)
    rows = mycursor.fetchall()
    list_of_list = [list(row) for row in rows]
    step = []
    for j in range(len(list_of_list)):
        res = ["" if i is None else i for i in list_of_list[j]]
        step.append(res)
    return step

def select(query):  #  for select 1 item
    mycursor.execute(query)
    rows = mycursor.fetchall()
    list_of_list = [list(row) for row in rows]
    step = []
    for j in range(len(list_of_list)):
        res = ["" if i is None else i for i in list_of_list[j]]
        step.append(res)
    return rows
class InserSqlObj:
    def __init__(self, table_name, column_name, field_var):
        self.query = ("insert into " + table_name + " (" + column_name + ") " + "values"
                      + " (\'" + field_var + "\')")
        #self.query = ("insert into " + table_name + " (" + column_name + ") " + "values"
                      # + " (\'" + field_var + "\')" + " ON DUPLICATE KEY UPDATE "
                      # + column_name + " =" + " \'" + field_var + "\'")
        print(self.query)

    def insert(self):
        mycursor.execute(self.query)


class UpdateSqlObj:
    def __init__(self, table_name, column_name, field_anchor, field_var, field_var_2):
        self.query = ("update " + table_name + " set " + column_name + " = " 
                      "\'" + field_var + "\'" + " where " + field_anchor +
                      " = " + "\'" + field_var_2 + "\'")

    def update(self):
        print(self.query)
        mycursor.execute(self.query)

#  ===================================================================================================
#  END of query definition



if __name__ == '__main__':
    pass
