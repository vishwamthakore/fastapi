#%%

import sqlite3

# Connect to the SQLite database
connection = sqlite3.connect('sql_app.db')

# Create a cursor object
cursor = connection.cursor()

cursor.execute("INSERT INTO posts (id, title, content) VALUES (?, ?, ?)", (1,"A", "B"))

connection.commit()

# Execute a query to get a list of tables
cursor.execute("SELECT * FROM sqlite_master")

# Fetch all the results
tables = cursor.fetchall()

# Print the list of tables
print(tables)

cursor.execute("SELECT * FROM posts;")

posts = cursor.fetchall()

# Print the list of tables
print(posts)



# Close the cursor and the connection
# cursor.close()
# connection.close()


#%%
