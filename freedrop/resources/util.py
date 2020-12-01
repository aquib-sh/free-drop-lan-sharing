import datetime

# Creates new table structure 
def set_table_structure(table_name):
    command = """CREATE TABLE {} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    path VARCHAR(500),
                    filename VARCHAR(200),
                    format VARCHAR(20),
                    creation DATETIME
                    );
                """.format(table_name)
    return command

# Returns current date for naming the file
def get_formatted_date():
        date_obj = datetime.datetime.now()
        date = date_obj.date()
        # Current formatted date
        formatted_date = str(date.day) + "-" + str(date.month) + "-" + str(date.year)
        return formatted_date