# Validate Input: https://stackabuse.com/flask-form-validation-with-flask-wtf/
# prepared statement:  in flask
# Parameterized Query avoid sql injection

# TODO : Parameterized Query avoid sql injection
#query = """Update employee set Salary = %s where id = %s""" 
# https://pynative.com/python-mysql-execute-parameterized-query-using-prepared-statement/
#tuple1 = (8000, 5)
#cursor.execute(query, tuple1)

# DONE: ABLE to give input text containing ' and " buy replacing with ‘ and “
# TODO: Need when reading need to replace with ' and "

import sys
import sqlite3

def get_create_table_query(table_name, **kwargs):
    query = "CREATE TABLE IF NOT EXISTS {} (".format(table_name)
    comma = ', '
    for key, value in kwargs.items():
        query = query + key + ' ' + value + comma
    query = query.rstrip(comma) + ");"
    return query

# get_create_table_query('store', item='TEXT', quantity='INTEGER', price='REAL')
        # CREATE TABLE IF NOT EXISTS store (item TEXT, quantity INTEGER, price REAL)

def get_insert_query(table_name,**kwargs):
    comma = r', '    
    Entry_Field =   ', '.join(list(kwargs.keys())) 
    Entry_Value = ''
    
    for key, value in kwargs.items():
        if isinstance(value, str): # type(value) == 'str': 
            value=value.replace("'",'‘') # remove any confusion in query you can re-cover the data when read query replace with ' or "
            value=value.replace('"','“') # remove any confusion in query           
            Entry_Value = Entry_Value + """'{}'{}""".format(str(value),comma)    
        else:
            Entry_Value = Entry_Value + """{}{}""".format(str(value),comma)    
    Entry_Value = Entry_Value.rstrip(comma)

    query = """INSERT INTO {} ({}) VALUES ({});""".format(table_name,Entry_Field, Entry_Value)        
#    print(query)
    return query

# get_insert_query('Song_Index' ,song_name = 'Nector of Instruction', song_short_name ='noi', sloka_statues=1)
        # >>>  "INSERT INTO Song_Index (song_name, song_short_name, sloka_statues) VALUES ('Nector of Instruction', 'noi', 1);"

def get_read_query(table_name, *args, **kwargs):
    if len(args) == 0: 
        query = "SELECT * FROM {}".format(table_name)
    else:
        # print(', '.join(args))
        query = "SELECT {} FROM {}".format(', '.join(args), table_name)

    if len(kwargs) != 0:
        cond_query=''
        for key, value in kwargs.items():
            if isinstance(value, str): # type(value) == 'str': 
                value=value.replace("'",'‘') # remove any confusion in query you can re-cover the data when read query replace with ' or "
                value=value.replace('"','“') # remove any confusion in query           

                cond_query =  """{} {}='{}'{} """.format(cond_query, key,value,' and')
            else:
                cond_query =  """{} {}={}{} """.format(cond_query, key,value,' and')                
        cond_query = cond_query.rstrip(' and') 
        query = query + ' WHERE ' + cond_query + ';'
    else:
        query += ';' 


#    print('get_read_query:' ,query)
    return query

# get_read_query('temp' )  # >>> SELECT * FROM temp;

# get_read_query('mySong', *['song_idx', 'slokas_no', 'sloka_hindi','slokas_id', 'sloka_eng'])
        # >>> SELECT song_idx, slokas_no, sloka_hindi, slokas_id, sloka_eng FROM mySong;

# get_read_query('mySong', *['song_idx', 'slokas_no', 'sloka_hindi','slokas_id', 'sloka_eng'], song_idx =4 , slokas_id=1)
        # >>> SELECT song_idx, slokas_no, sloka_hindi, slokas_id, sloka_eng FROM mySong WHEN  song_idx=4 and  slokas_id=1;

def get_update_query(table_name, *args, **kwargs):
    query = "UPDATE {} SET ".format(table_name)

    if len(args) == 0: 
        last_key = list(kwargs.keys())[-1]
        if isinstance(kwargs[last_key], str):
            cond_query = " WHERE {}='{}'".format(last_key, kwargs[last_key])
        else:
            cond_query = " WHERE {}={}".format(last_key, kwargs[last_key])
        del kwargs[last_key]
    else: 
        
        cond_query = " WHERE "
        for key in args:
            if isinstance(kwargs[key], str):
                cond_query =  """{} {}='{}'{} """.format(cond_query, key,kwargs[key],' and')
            else:
                cond_query =  """{} {}={}{} """.format(cond_query, key,kwargs[key],' and')                
            del kwargs[key]
        cond_query = cond_query.rstrip(' and') 
            
    
    comma = ', '
    for key, value in kwargs.items():
        if isinstance(value, str):
            value=value.replace("'",'‘') # remove any confusion in query you can re-cover the data when read query replace with ' or "
            value=value.replace('"','“') # remove any confusion in query           
            query =  """{} {}='{}'{} """.format(query, key,value,comma)  #  query + str(key) + '=' + str(value) + comma
        else:
            query =  """{} {}={}{} """.format(query, key,str(value),comma)  

    query = query.rstrip(comma) 
    
    query += cond_query
#    print(query)
    return query
    
# get_update_query('store', quantity=10, price=15, item='indian mango')
        # UPDATE store SET quantity=10, price=15 WHERE item='indian mango'
# get_update_query('store', quantity=10, price=15, item=10)
        # UPDATE store SET quantity=10, price=15 WHERE item=10

def get_delete_query(table_name, **kwargs):
    # if len(kwargs) > 1:
    cond_query = ""
    for key, value in kwargs.items():
        if isinstance(value, str): # type(value) == 'str': 
            cond_query = cond_query + """{}='{}'{}""".format(key, str(value),' and ')    
        else:
            cond_query = cond_query + """{}={}{}""".format(key, str(value),' and ')    
    cond_query = cond_query.rstrip(' and ')
        
    # table_index = list(kwargs.keys())[0]
    query = "DELETE FROM {} WHERE {};".format(table_name, cond_query )
    # print(query)
    return query

# get_delete_query('Song', song_idx=1,sloka_no = 5)
    # >>> 'DELETE FROM Song WHERE song_idx=1 and sloka_no=5;'

class SqliteModel():
    def __init__(self,db_path,table_name):
        self.db_path = db_path
        self.table_name = table_name
        self.db_connect = sqlite3.connect(db_path) # OperationalError: database is locked may occur to reduce try  <db.connections.close_all()>
                                                # https://www.geeksforgeeks.org/how-to-list-tables-using-sqlite3-in-python/?ref=lbp
    
    def create_table(self, **kwargs):
        # self.db_connect = sqlite3.connect(db_path)
        self.db_cursor = self.db_connect.cursor()
        query = get_create_table_query(self.table_name, **kwargs)
        try :
            self.db_cursor.execute(query)
            self.db_connect.commit()
            # auto_increment and delete on cascade https://stackoverflow.com/questions/29037793/sqlite-integrityerror-unique-constraint-failed
            self.db_cursor.close()
            # self.db_connect.close()
        except sqlite3.Error as e:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info() 

        finally:
            self.db_cursor.close()
            print('Table : {} Created Successful !'.format(self.table_name))

    def create_entry(self, **kwargs):
        query = get_insert_query(self.table_name,**kwargs)
        self.db_cursor = self.db_connect.cursor()
        # print(query)
        try :
            self.db_cursor.execute(query)        
            self.db_connect.commit()
        except sqlite3.IntegrityError as e:
            # print('Exception: {}'.format(e))   # >>>  Exception: UNIQUE constraint failed: SongIndex.song_short_name
            print('Can\'t Create new Entry! Already Existing Entry!',' '.join(e.args))                      # >>> ('UNIQUE constraint failed: SongIndex.song_short_name',)
            # print('Exception: %s' % (' '.join(e.args)))   # >>> UNIQUE constraint failed: SongIndex.song_short_name
            # print("Exception class is: ", e.__class__)  # >>> Exception class is:  <class 'sqlite3.IntegrityError'>
    
            # print('SQLite traceback: ')
            # exc_type, exc_value, exc_tb = sys.exc_info()
            # print(sys.exc_info())
                # >>> (<class 'sqlite3.IntegrityError'>, IntegrityError('UNIQUE constraint failed: SongIndex.song_short_name'), <traceback object at 0x7fce51c32b80>)
            # print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")
                 # >>> IntegrityError at line 154 of /media/karthik/myVolume/workspace/workspae_vedabase/slokabase/SqliteModel.py: UNIQUE constraint failed: SongIndex.song_short_name


        finally:
            self.db_cursor.close()      
    
    def read_entry(self, *args, **kwargs):
        # query = "SELECT * FROM {};".format(self.table_name)
        query = get_read_query(self.table_name, *args,**kwargs)
#        print(query)
        self.db_cursor = self.db_connect.cursor()
        try :
            self.db_cursor.execute(query)
            columns = [column[0] for column in self.db_cursor.description]
            data = [dict(zip(columns, row)) for row in self.db_cursor.fetchall()]
            # print(data)
            # rows = self.db_cursor.fetchall()
            # for row in rows:
            #     print(row)

        except sqlite3.Error as e:
            print('Exception: {}'.format(e))
        finally:
            self.db_cursor.close()
        return data

    def update_entry(self,*args, **kwargs):
        query = get_update_query(self.table_name,*args,**kwargs)
        self.db_cursor = self.db_connect.cursor()
        # print(query)
        try :
            self.db_cursor.execute(query)        
            self.db_connect.commit()
        except sqlite3.Error as e:
            print('Exception: {}'.format(e))

        finally:
            self.db_cursor.close()

    def delete_entry(self, **kwargs):
        self.db_cursor = self.db_connect.cursor()    
        query = get_delete_query(self.table_name, **kwargs)
        print(query)
        try :
            self.db_cursor.execute(query)        
            self.db_connect.commit()
        except sqlite3.Error as e:
            print('Exception: {}'.format(e))

        finally:
            self.db_cursor.close()
            
    def delete_table(self):
        self.db_cursor = self.db_connect.cursor()        
        query = 'DROP TABLE IF EXISTS {};'.format(self.table_name)
        print(query)
        try :
            self.db_cursor.execute(query)        
            self.db_connect.commit()
        except sqlite3.Error as e:
            print('Exception: {}'.format(e))

        finally:
            self.db_cursor.close()

    def custom_query(self,query):
        # db_connect = self.db_connect
        # db_cursor = db_connect.cursor()
        db_cursor =self.db_connect.cursor()
        # query = f"""UPDATE {self.table_name} SET synonyms= null WHERE song_idx={mysong_index};"""
        try :
            db_cursor.execute(query)
            self.db_connect.commit()
            # auto_increment and delete on cascade https://stackoverflow.com/questions/29037793/sqlite-integrityerror-unique-constraint-failed

# TODO: If you want some return or output create your own custom_query function which will return the data
#            data = db_cursor.fetchall()
#            print(data)    
            db_cursor.close()            
        except sqlite3.Error as e:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info() 
        
        finally:
            db_cursor.close()
            print('Run custom query:{} \nSuccessful !'.format(query))





    def db_close(self):
        self.db_connect.close()

    def __del__( self):
        #  print('Closed Connection to db')
         self.db_connect.close()           
