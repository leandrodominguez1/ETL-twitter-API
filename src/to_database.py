import psycopg2
import csv
import logging
from decouple import config as c

def create_table(cursor, conn, account):
    SQLquery = '''
        CREATE TABLE IF NOT EXISTS twitter_data_{} (
            username VARCHAR(500),
            text VARCHAR(500),
            favorite_count INT,
            retweet_count INT,
            created_at TIMESTAMP,
            id_str VARCHAR(20),
            PRIMARY KEY(created_at, id_str)
        );
    '''.format(account)
    cursor.execute(SQLquery)
    conn.commit()

def load_data(archivo,account):
 
    conn_string = f" host={c('DB_HOST')} dbname={c('DB_NAME')} user={c('DB_USER')} password={c('DB_PASSWORD')} "
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    logging.info("Connected to database!\n")

    create_table(cursor,conn,account)

    with open(archivo, 'r', encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            username = row[1]  
            text = row[2]
            favorite_count = int(row[3])
            retweet_count = int(row[4])
            created_at = row[5]
            id_str = row[6]

            SQLquery = '''
                INSERT INTO twitter_data_{} (username, text, favorite_count, retweet_count, created_at, id_str)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (created_at, id_str) DO NOTHING;
            '''.format(account)

            cursor.execute(SQLquery, (username, text, favorite_count, retweet_count, created_at, id_str))

    csv_file.close()
    conn.commit()
    conn.close()
