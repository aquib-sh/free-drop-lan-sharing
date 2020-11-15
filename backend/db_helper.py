""" AUTHOR: SHAIKH AQUIB
    THIS WILL SERVER AS A SET OF HELPFUL FUNCTIONS TO MAKE DATABASE OPERATIONS EASIR IN SERVER
"""

class DBHelper:

    def __init__(self, cursor):
        self.cursor = cursor

    # Fetches the cursor and returns list
    def fetch_list(self):
        return [item[0] for item in cursor.fetchall()]

    # Checks if path already exists in the table
    def path_already_exists(self, path_name, table_name):
        cursor.execute('SELECT PATH FROM {} WHERE PATH="{}"'.format(table_name, path_name))
        if len(fetch_list()) == 0:
            return False
        return True

    # Returns the list of path  names from the searched path
    def get_path(self, path_name, table_name):
        cursor.execute('SELECT PATH FROM {} WHERE PATH="{}"'.format(table_name, path_name))
        return fetch_list()

    # Returns the list of path names from the searched path with regular expressions
    def search_path(self, path_name, table_name):
        cursor.execute('SELECT PATH FROM {} WHERE PATH REGEXP "{}"'.format(table_name, path_name))
        return fetch_list()

    # Insert into table
    def insert_value(self, table, path, file_format, creation):
        cursor.execute("""INSERT INTO {0} (path, format, creation) 
            VALUES ("{1}", "{2}", "{3}")
            """).format(table, path, file_format, creation))