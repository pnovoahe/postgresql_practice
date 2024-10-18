import os
import psycopg2
from flask import Flask, render_template, request, url_for, redirect

db_host = os.getenv("POSTGRES_HOST", "postgres")
db_name = os.getenv("POSTGRES_DB", "flask_db")
db_user = os.getenv("POSTGRES_USER", "admin")
db_password = os.getenv("POSTGRES_PASSWORD", "admin123")

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host=db_host,
        	database=db_name,
		user=db_user,
        password=db_password)
    return conn


@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM books ORDER BY id;')
        books = cur.fetchall()
    except Exception as e:
        error_message = f'Error when connecting with the database: {str(e)}'
        return render_template('error.html', error_message=error_message)
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
    return render_template('index.html', books=books)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':

        try:
            title = request.form['title']
            author = request.form['author']
            pages_num = int(request.form['pages_num'])
            review = request.form['review']
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO books (title, author, pages_num, review)'
            'VALUES (%s, %s, %s, %s)',
            (title, author, pages_num, review))
            conn.commit()
        except Exception as e:
            error_message = f'Ha ocurrido un error en la entrada de los datos. Por favor, revise que no se estén vacíos los campos: {str(e)}'
            return render_template('error.html', error_message=error_message)
        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/delete/', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        book_id = request.form['book_id']
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            sql_del = 'DELETE FROM books WHERE id = %s'
            cur.execute(sql_del, (book_id,))
            
            # Verifica si se eliminó alguna fila
            if cur.rowcount == 0:
                # No se encontró el libro con el ID dado
                return render_template('error.html', error_message='The book with id {} does not exist.'.format(book_id))
            
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('index'))  # Redirige a la página principal
        except Exception as e:
            error_message = f'Error al eliminar el libro: {str(e)}'
            return render_template('error.html', error_message=error_message)
    
    return render_template('delete.html')


@app.route('/update/<int:book_id>', methods=['GET', 'POST'])
def update(book_id):
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pages_num = request.form['pages_num']
        review = request.form['review']
        
        try:
            cur.execute('UPDATE books SET title = %s, author = %s, pages_num = %s, review = %s WHERE id = %s',
                        (title, author, pages_num, review, book_id))
            conn.commit()
            return redirect(url_for('index'))  # Redirige a la página principal
        except Exception as e:
            # Redirige a una página de error personalizada
            error_message = f'Error al actualizar el libro: {str(e)}'
            return render_template('error.html', error_message=error_message)

    # Carga los datos actuales del libro
    cur.execute('SELECT * FROM books WHERE id = %s', (book_id,))
    book = cur.fetchone()
    cur.close()
    conn.close()

    return render_template('update.html', book=book)