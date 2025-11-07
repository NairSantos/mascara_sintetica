##
import sqlite3
import pandas as pd

conn = sqlite3.connect("data.db")
df = pd.read_sql_query("SELECT * FROM users", conn)
print(df.head(50))
conn.close()
