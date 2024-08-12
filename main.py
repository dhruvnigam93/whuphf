from fasthtml.common import *
import sqlite3

app, rt = fast_app(live=True)


@rt('/', methods=['GET'])
def index():
    return Div(
        Form(
            Input(type='text', name='query', placeholder='Search...'),
            Button('Search', type='submit'),
            method='GET',
            action='/search'
        )
    )


@rt('/search', methods=['GET'])
def search(query):
    conn = sqlite3.connect('office-lines.db')
    c = conn.cursor()
    c.execute('SELECT line_text FROM main.items limit 1')
    results = c.fetchall()
    conn.close()

    return Div(
        P(f'Search results for "{query}":'),
        Ul(*[Li(result[0]) for result in results])
    )


serve()