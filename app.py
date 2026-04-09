from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    # เชื่อมต่อกับไฟล์ noodle.db
    conn = sqlite3.connect('noodle.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    
    # ดึงข้อมูลสินค้าจากตาราง products [cite: 495]
    products = conn.execute('SELECT * FROM products').fetchall()
    
    # ดึงข้อมูลหมวดหมู่ [cite: 497]
    categories = conn.execute('SELECT * FROM categories').fetchall()
    
    conn.close()
    return render_template('index.html', products=products, categories=categories)

@app.route('/menu')
def view_menu():
    conn = get_db_connection()
    # ดึงข้อมูลจากตาราง menu [cite: 498]
    menus = conn.execute('SELECT * FROM menu').fetchall()
    conn.close()
    return render_template('menu.html', menus=menus)

if __name__ == '__main__':
    app.run(debug=True)
