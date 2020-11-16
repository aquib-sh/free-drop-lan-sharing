""" AUTHOR: SHAIKH AQUIB
    THIS WILL SERVER AS A SET OF HELPFUL FUNCTIONS TO MAKE DATABASE OPERATIONS EASIR IN SERVER
"""

class DBHelper:

    def __init__(self, cursor):
        self.cursor = cursor

    # Fetches the cursor and returns list
    def fetch_list(self):
        return [item[0] for item in self.cursor.fetchall()]

    # Checks if path already exists in the table
    def path_already_exists(self, path_name, table_name):
        self.cursor.execute('SELECT PATH FROM {} WHERE PATH="{}"'.format(table_name, path_name))
        if len(self.fetch_list()) == 0:
            return False
        return True

    # Returns the list of path  names from the searched path
    def get_path(self, path_name, table_name):
        self.cursor.execute('SELECT PATH FROM {} WHERE PATH="{}"'.format(table_name, path_name))
        return self.fetch_list()

    # Returns file format
    def get_format(self, path_name, table_name):
        self.cursor.execute('SELECT format FROM {} WHERE path="{}"'.format(table_name, path_name))
        return self.fetch_list()

    # Returns the list of path names from the searched path with regular expressions
    def search_path(self, path_name, table_name):
        self.cursor.execute('SELECT PATH FROM {} WHERE PATH REGEXP "{}"'.format(table_name, path_name))
        return self.fetch_list()

    # Returns a list of an entire column from table present on server database
    def get_full_list(self, column_name, table_name):
        self.cursor.execute('SELECT {} FROM {}'.format(column_name, table_name))
        return self.fetch_list()

    # Insert into table
    # creation date will always be the current one
    def insert_value(self, table, path, file_format):
        self.cursor.execute("""INSERT INTO {0} (path, format, creation) 
            VALUES ("{1}", "{2}", NOW())
            """.format(table, path, file_format))