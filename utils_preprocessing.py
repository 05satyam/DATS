def escape_special_characters(word):
    return word.replace('%', '\\%').replace('_', '\\_')


def construct_dynamic_word_by_word_sql_query(table_name, user_query, column_names):
    words = [escape_special_characters(word) for word in user_query.split()]
    quoted_column_names = [f'CAST("{col}" AS VARCHAR)' for col in column_names]

    like_clauses = []
    for word in words:
        word_like_clauses = [f"{col} LIKE '%{word}%'" for col in quoted_column_names]
        like_clauses.append('(' + ' OR '.join(word_like_clauses) + ')')

    # Combine word LIKE clauses with AND, as we want each word to be found somewhere
    combined_like_clause = ' OR '.join(like_clauses)
    sql_query = f"SELECT * FROM {table_name} WHERE {combined_like_clause};"

    return sql_query

def search_tables_for_query(conn, user_query):
    # Get all table names
    tables = conn.execute("SHOW TABLES").fetchall()

    results = {}

    for table in tables:
        table_name = table[0]
        columns = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
        column_names = [column[1] for column in columns]  # Column names are at index 1
        sql_query=construct_dynamic_word_by_word_sql_query(table_name, user_query, column_names)
        matched_rows = conn.execute(sql_query).fetchall()
        if matched_rows:
            results[table_name] = matched_rows

    return results


def escape_special_characters(user_query):
    return user_query.replace('%', '\\%').replace('_', '\\_')
