import sqlite3

with sqlite3.connect("database/log.db") as connection:
    cursor = connection.cursor()
    cursor.execute("""DROP TABLE Log""")
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Log(
    writer_discord_id CHAR(18),
    wroten_name VARCHAR(9),
    column_name VARCHAR(10),
    point INT,
    writed_at DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    cursor.execute("SELECT * FROM Log")
    data = cursor.fetchall()
    print(data)
