from duckdb import duckdb
from db import initialize_db, display_onerow_data_from_alltables
from model import llm
from utils_preprocessing import escape_special_characters, search_tables_for_query
from flask import Flask, request, render_template
import duckdb

app = Flask(__name__)

@app.route('/load-data', methods=['GET', 'POST'])
def load_data():
    if request.method == 'POST':
        folder_path = request.form.get('folder_path')
        conn = duckdb.connect(database='my_data.duckdb', read_only=False)
        initialize_db(folder_path, conn)
        conn.close()
        return render_template('index.html', message="Data loaded successfully!")
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        user_query = request.form.get('query')
        user_query = escape_special_characters(user_query)
        conn = duckdb.connect(database='my_data.duckdb', read_only=False)
        result = search_tables_for_query(conn, user_query)
        conn.close()
        combined_data = " ".join(["".join(str(value).strip() for value in row) for table_rows in result.values() for row in table_rows])
        insight_query = llm(combined_data, user_query)
        # print("insight_query  ", insight_query)
        return render_template('index.html', user_query=user_query, insight_query=insight_query)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)

