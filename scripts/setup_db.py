import sqlite3
import csv


def infer_schema(header, sample_data) -> str:
    """
    Infer schema for SQLite table based on sample data
    :param header:
    :param sample_data:
    :return:
    """
    schema = []
    for i, column in enumerate(header):
        # Infer type based on sample data
        col_type = 'TEXT'
        for row in sample_data:
            if isinstance(row[i], int):
                col_type = 'INTEGER'
            elif isinstance(row[i], float):
                col_type = 'REAL'
            else:
                col_type = 'TEXT'
                break
        schema.append(f'{column} {col_type}')
    return ', '.join(schema)


def setup_database():
    """
    Setup SQLite database and import data from CSV
    :return:
    """
    conn = sqlite3.connect('office-lines.data')
    c = conn.cursor()

    with open('the-office-lines - scripts.csv', 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Get header row
        sample_data = [next(reader) for _ in range(5)]  # Read first 5 rows for type inference
        schema = infer_schema(header, sample_data)
        c.execute(f'CREATE TABLE IF NOT EXISTS items ({schema})')

        # Reset reader and skip header again
        file.seek(0)
        next(reader)
        data = [tuple(row) for row in reader]

    placeholders = ', '.join(['?' for _ in header])
    c.executemany(f'INSERT INTO items VALUES ({placeholders})', data)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    setup_database()
