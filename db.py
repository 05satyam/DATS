import glob
import os
import zipfile
import pandas as pd
import duckdb

def initialize_db(folder_path, conn):
    conn.execute("BEGIN TRANSACTION;")
    initialize_db_from_csv_zip1(folder_path, conn)
    conn.execute("COMMIT;")

def sanitize_table_name(filename):
    filename=filename.replace(" ", '_')
    return filename.split('/')[-1].replace('-', '_').replace('.', '_')

def sanitize_column_names(df):
    df.columns = [str(col).replace(' ', '_').replace('-', '_').replace('.', '_') for col in df.columns]
    return df

def is_data_line(line, total_columns):
    return len(line.split(',')) < total_columns


def read_csv_with_minimum_columns(df):
    total_columns=df.shape[1]
    df = df[df.apply(lambda x: x.count() >= total_columns, axis=1)]
    return df


def initialize_db_from_csv_zip1(zip_path, conn):
    for filename in os.listdir(zip_path):
        if filename.endswith('.csv') and not filename.startswith('.'):
                file_path = os.path.join(zip_path, filename)
                # print("file_path", file_path)
                try:
                        df = pd.read_csv(file_path, encoding='ISO-8859-1')
                        df = df.iloc[1:]
                        df = df.drop(df.columns[0], axis=1)
                        df = df.reset_index(drop=True)
                        df = read_csv_with_minimum_columns(df)

                        df = df.dropna()
                        df = df[~df.map(lambda x: '.pdf' in str(x)).any(axis=1)]
                        if not df.empty:
                            table_name = sanitize_table_name(file_path)
                            df = sanitize_column_names(df)
                            conn.register(table_name, df)
                            conn.execute(f"CREATE TABLE  {table_name} AS SELECT * FROM '{table_name}'")

                except Exception as e:
                    print(f"Skipping file due to encoding error: {filename}, Error: {e}")


def display_onerow_data_from_alltables(conn):
    tables = conn.execute("SHOW TABLES").fetchall()

    for table in tables:
        table_name = table[0]
        entry = conn.execute(f"SELECT * FROM {table_name}").fetchone()
        # print(f"Entry from {table_name}: {entry}")



#initialize_db_from_csv_zip1("/dummy_path/Complete_LinkedInDataExport_", conn)
# conn = duckdb.connect(database='my_data.duckdb', read_only=True)
# display_onerow_data_from_alltables(conn)