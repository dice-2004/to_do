import sqlite3

###################################################################################################################################################################
#####################################################   これはDB内を簡易的に確認するためのプログラムファイルです   ###################################################
###################################################################################################################################################################

DATABASE = 'DB.db'

def list_tables_and_contents():
    con = sqlite3.connect(DATABASE)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        print(f"Contents of table {table[0]}:")
        cursor.execute(f"SELECT * FROM {table[0]};")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        print("\n")  # テーブル間に空行を挿入
    con.close()

if __name__ == "__main__":
    list_tables_and_contents()
