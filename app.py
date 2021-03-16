import os
from dotenv import load_dotenv
import sqlite3
from sqlite3 import Error
from werkzeug.datastructures import FileStorage
load_dotenv()

def convert_into_binary(file_path):
  print("[INFO] : converting into binary data rn")
  with open(file_path, 'rb') as file:
    binary = file.read()
  return binary

def write_to_file(binary_data, file_name):
  # dud_name = "converted_" + file_name
  with open(file_name, 'wb') as file:
    file.write(binary_data)
  print("[DATA] : The following file has been written to file: ", file_name)

def read_blob_data(entryID):
  try:
    conn = sqlite3.connect('app.db')
    conn.text_factory = str  
    cur = conn.cursor()
    print("[INFO] : Connected to SQLite to read_blob_data")
    sql_fetch_blob_query = """SELECT * from uploads where id = ?"""
    cur.execute(sql_fetch_blob_query, (entryID,))
    record = cur.fetchall()
    for row in record:
      converted_file_name = row[1]
      photo_binarycode  = row[2]
      # parse out the file name from converted_file_name

      # converted_file_name 
      dud_file_name = "parsedfilenamehere" + ".png"

      write_to_file(photo_binarycode, dud_file_name)
      print("[DATA] : Image successfully stored on disk. Check the project directory. \n")
    cur.close()
  except sqlite3.Error as error:
    print("[INFO] : Failed to read blob data from sqlite table", error)
  finally:
    if conn:
        conn.close()

def insert_into_database(file_path_name, file_name_blob): 
  try:
    conn = sqlite3.connect('app.db')
    conn.text_factory = str   
    print("[INFO] : Successful connection!")
    cur = conn.cursor()
    insert_file = '''INSERT INTO uploads(file_names, file_blob)
      VALUES(?, ?)'''
    cur = conn.cursor()
    cur.execute(insert_file, (file_path_name, file_name_blob, ))
    conn.commit()
    print("[INFO] : the blob for ", file_path_name, " is in the database.") 
  except Error as e:
    print(e)
  finally:
    if conn:
      conn.close()
    else:
      error = "Welp something is wrong here."

def retrieve_file(entryID):
  try:
    conn = sqlite3.connect('app.db')
    conn.text_factory = str   # added in to get rid of "u must not use 8 bit blah blah"
    print("[INFO] : Successful connection!")
    cur = conn.cursor()
    sql_retrieve_file_query = """SELECT * FROM uploads WHERE id = ?"""   
    cur.execute(sql_retrieve_file_query, (entryID,))
    record = cur.fetchone()
    record_blob = record[2]    
    read_blob_data(entryID)
  except Error as e:
    print(e)
  finally:
    if conn:
      conn.close()
    else:
      error = "how tf did u get here."

def main():
  print("Hello World!")
  file_path_name = raw_input("Enter full file path:\n") 
  # file_path_name = "/Users/diane/Documents/DRAW_THE_OWL_MEME.png"
  print("[DATA] : ", file_path_name) 
  file_name_blob = convert_into_binary(file_path_name)
  print("[INFO] : the last 100 characters of blob = ", file_name_blob[:100]) 
  # insert_into_database(file_path_name, file_name_blob)
  retrieve_file(1)

if __name__ == "__main__":
  main()
