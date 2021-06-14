import mysql
from mysql.connector import MySQLConnection, Error
from operator import itemgetter


class Database:
    def __init__(self, text):
        self.text = text

    def connect(self):
        """ Connect to MySQL database """
        conn = None
        try:
            conn = mysql.connector.connect(host='localhost',
                                           database='platenumbers',
                                           user='root',
                                           password='123456',
                                           autocommit=True)
            if conn.is_connected():

                print('Connected to MySQL database')
                mycursor = conn.cursor()
                plate_num = (self.text)



                #check whether to enter or exit

                check_database = ("""SELECT platenumberlist FROM
                 platenumbers where platenumberlist = (%s) LIMIT 1""")

                mycursor.execute(check_database, (plate_num,))

                if mycursor.fetchone():
                    flag = False
                else:
                    flag = True


                # add
                #enter the garage
                if flag:
                    mySql_insert_query = """INSERT INTO platenumbers (platenumberlist)
                                             VALUES 
                                             (%s) """

                    mycursor.execute(mySql_insert_query, (plate_num,))

                # delete
                #exit the garage

                elif not flag:
                    mySql_Delete_query = """Delete from platenumbers where platenumberlist = (%s) """


                    mycursor.execute(mySql_Delete_query, (plate_num,))
                conn.close()
                return flag



        except Error as e:
            print(e)

        finally:
            if conn is not None and conn.is_connected():
                conn.close()



"""         Necessary params      """

# print(mycursor.rowcount, "record inserted.")

# mycursor.execute("CREATE TABLE platenumbers (name VARCHAR(255), address VARCHAR(255))") - already exists
# mycursor.execute("ALTER TABLE platenumbers ADD platenumberslist")

# mycursor.execute("ALTER TABLE platenumbers ADD platenumberlist VARCHAR(100) NOT NULL")
# mycursor.execute("ALTER TABLE platenumbers DROP platenumberlist")


# mycursor.execute("""INSERT INTO platenumbers(platenumberlist)
#                   VALUES ('%s')""" % (self.text))
# mycursor.execute("""INSERT INTO platenumbers(platenumberlist)
#                            VALUES ('%s')""" % (self.text))
# mycursor.execute("""INSERT INTO platenumbers(platenumberlist)
#                            VALUES ('%s')""" % (self.text))

# mycursor.execute("TRUNCATE TABLE platenumbers")
