import mysql.connector
from mysql.connector import errorcode


class DatabaseManager:
    """
    Class for working with MySQL (Database Management System)
    """
    def __init__(self, database, table_name, username, password, host):
        self.database = database
        self.table_name = table_name
        self.username = username
        self.password = password
        self.host = host
        self.dbms_connect = None
        self.connect_to_dbms()
        self.cursor = self.dbms_connect.cursor()
        self.connect_to_db()
        self.create_table()

    def connect_to_dbms(self):
        """
        Connect to MySQL (Database Management System)
        """
        try:
            self.dbms_connect = mysql.connector.connect(user=self.username, password=self.password, host=self.host)
            print('Successfully connected to MySQL')
        except mysql.connector.Error as e:
            print("Can't connect to your MySQL dbms")
            print(e)

    def connect_to_db(self):
        """
        Connect to selected database
        """
        try:
            self.cursor.execute('USE {0}'.format(self.database))
            print('Connected to {0}'.format(self.database))
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_db()
                print('Database {0} created successfully'.format(self.database))
                self.dbms_connect.database = self.database
            else:
                print(e.msg)

    def create_db(self):
        """
        Create database
        """
        try:
            self.make_request("CREATE DATABASE {0} DEFAULT CHARACTER SET 'utf8'".format(self.database))
        except mysql.connector.Error as e:
            print('Failed creating database: {0}'.format(e))

    def make_request(self, command):
        """
        Make request to database
        """
        try:
            self.cursor.execute(command)
            print('Successfully: {0}'.format(command))
        except mysql.connector.Error as e:
            print('Failed with {0}'.format(command))
            print(e.msg)
            self.dbms_connect.rollback()
            return e
        try:
            data = self.cursor.fetchall()
        except mysql.connector.Error:
            data = self.cursor.fetchone()
        return data

    def create_table(self):
        """
        Create a table in the database if it doesn't already exist
        """
        command = (" CREATE TABLE IF NOT EXISTS `{0}` ("
                   " `id` int(4) NOT NULL AUTO_INCREMENT,"
                   " `name` char(100) UNIQUE ,"
                   " `price` varchar(100),"
                   " `link` varchar(150),"
                   " `description` varchar(250),"
                   " PRIMARY KEY (`id`)"
                   ") ENGINE=InnoDB".format(self.table_name))
        self.make_request(command)

    def add_wish(self, name, price, link, description):
        """
        Add new wish to database
        """
        try:
            command = "INSERT INTO `{0}` (`name`, `price`, `link`, `description`)".format(self.table_name)
            command += " VALUES ('{0}', '{1}', '{2}', '{3}')".format(name, price, link, description)
            self.make_request(command)
            self.dbms_connect.commit()
            return True
        except mysql.connector.Error:
            return False

    def get_wishes(self):
        """
        Get all wishes from database
        """
        self.create_table()
        return self.make_request("SELECT * FROM `{0}`".format(self.table_name))

    def edit_wish(self, wish_name, fields):
        """
        Edit selected wish from database
        """
        try:
            command = "UPDATE `{0}` SET `name`= '{1}', `price`='{2}',`link`='{3}', `description`='{4}'" \
                      " WHERE `name`='{5}'" \
                .format(self.table_name, fields[0], fields[1], fields[2], fields[3], wish_name)
            self.make_request(command)
            self.dbms_connect.commit()
            return True
        except mysql.connector.Error:
            return False

    def delete_wish(self, wish_name):
        """
        Delete selected wish from database
        """
        try:
            command = "DELETE FROM `{0}` WHERE `name`='{1}'".format(self.table_name, wish_name)
            self.make_request(command)
            self.dbms_connect.commit()
            return True
        except mysql.connector.Error:
            return False