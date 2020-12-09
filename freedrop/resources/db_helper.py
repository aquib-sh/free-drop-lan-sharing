""" AUTHOR: SHAIKH AQUIB
    THIS WILL SERVER AS A SET OF HELPFUL FUNCTIONS TO MAKE DATABASE OPERATIONS EASIR IN SERVER
"""
import sys


class DBHelper:

    def __init__(self, cursor):
        self.cursor = cursor

    def fetch_list(self):
        """ Fetches the cursor and returns list. """
        return [item[0] for item in self.cursor.fetchall()]

    def path_already_exists(self, path_name, table_name):
        """ Checks if path already exists in the table. """
        self.cursor.execute('SELECT PATH FROM {} WHERE PATH="{}"'.format(table_name, path_name))
        if len(self.fetch_list()) == 0:
            return False
        return True

    def get_path(self, path_name, table_name):
        """ Returns the list of path  names from the searched path. """
        self.cursor.execute('SELECT PATH FROM {} WHERE FILENAME="{}"'.format(table_name, path_name))
        return self.fetch_list()

    def get_format(self, path_name, table_name):
        """ Returns file format. """
        if sys.platform == "win32":
            path_name = path_name.replace("\\", r"\\")
        self.cursor.execute('SELECT format FROM {} WHERE path="{}"'.format(table_name, path_name))
        return self.fetch_list()

    def search_path(self, path_name, table_name):
        """ Returns the list of path names from the searched path with regular expressions. """
        self.cursor.execute('SELECT PATH FROM {} WHERE PATH REGEXP "{}"'.format(table_name, path_name))
        return self.fetch_list()

    def get_full_list(self, column_name, table_name):
        """ Returns a list of an entire column from table present on server database """
        self.cursor.execute('SELECT {} FROM {}'.format(column_name, table_name))
        return self.fetch_list()

    def insert_value(self, table, path, file_format):
        """ 
            Inserts record into the database 
            by formatting the path according to 
            the current operating system.
        """
        if sys.platform == "win32":
            filename = path.split("\\")[-1]
            path     = path.replace("\\", r"\\")
        elif sys.platform == "linux":
            filename = path.split("/")[-1]

        self.cursor.execute("""INSERT INTO {0} (path, filename, format, creation) 
            VALUES ("{1}", "{2}", "{3}", NOW())
            """.format(table, path, filename, file_format))

    def delete_value(self, table, filename):
        """ Delete records from table. """
        self.cursor.execute('DELETE FROM {} WHERE filename="{}"'.format(table, filename))

    def update_value(self, table, column, current_value, new_value):
        """ Delete records from table. """
        self.cursor.execute('UPDATE {tab} SET {col}="{new_val}" WHERE {col}="{cur_val}"'.format(
            tab     = table, 
            col     = column, 
            cur_val = current_value, 
            new_val = new_value)
            )
