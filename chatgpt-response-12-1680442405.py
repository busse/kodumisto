Unfortunately, as an AI language model, I do not have direct access to a Peoplesoft instance for testing purposes. However, I can provide an example SQL query and some Python code snippets that could be used to connect to a Peoplesoft database using a Python library called pyodbc.

Here is an example SQL query that could be used to get the desired report:

```
SELECT VENDOR_ID, VENDOR_NAME, STATUS
FROM PS_VENDOR
ORDER BY VENDOR_NAME
```

This query should return all vendors from the PS_VENDOR table, sorted by their name, along with a column indicating whether each vendor is Active or Inactive.

To execute this query from Python using pyodbc, you would need to first install pyodbc (if you haven't already) and configure a connection to your Peoplesoft database. Here is some sample code to get you started:

```
import pyodbc

# set up database connection
connection = pyodbc.connect(
    'DRIVER={your_database_driver_here};SERVER={your_database_server_here};'
    'DATABASE={your_database_name_here};UID={your_username_here};PWD={your_password_here}'
)

# define the SQL query to execute
sql_query = '''
    SELECT VENDOR_ID, VENDOR_NAME, STATUS
    FROM PS_VENDOR
    ORDER BY VENDOR_NAME
'''

# execute the query and fetch the results
cursor = connection.cursor()
cursor.execute(sql_query)
results = cursor.fetchall()

# print the results
for row in results:
    print(row)
``` 

You would need to replace the placeholders in the `connection` variable with the appropriate values for your Peoplesoft instance, and adjust the column names and table names in the SQL query if necessary.

Once you have executed the query and fetched the results, you can manipulate them further in Python as needed to generate the desired report output.