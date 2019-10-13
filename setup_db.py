import sqlite3


conn = sqlite3.connect('lms.db')

c = conn.cursor()

sql_create_collection_table = """ CREATE TABLE IF NOT EXISTS collection (
                                        lego_id integer,
                                        name text,
                                        purchase_price real,
                                        estimated_selling_price real,
                                        actual_selling_price real,
                                        quantity integer


                                    ); """

c.execute(sql_create_collection_table)

conn.commit()

conn.close()