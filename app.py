from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

# กำหนด Path ของฐานข้อมูลให้ถูกต้องสำหรับ PythonAnywhere
# หากรันในเครื่องตัวเอง สามารถเปลี่ยนเป็น 'noodle.db' ได้ครับ
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'noodle.db')

def get_db_connection():
    """ฟังก์ชันเชื่อมต่อกับฐานข้อมูล SQLite"""
    conn = sqlite3.connect(DB_PATH)
    # ตั้งค่าให้เรียกดูข้อมูลแบบ Dictionary (Row objects) 
    # เพื่อให้ตรงกับ index.html ที่เรียกใช้ product['name']
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        
        # ดึงข้อมูลจากตาราง products
        # หมายเหตุ: ในไฟล์ HTML มีการเรียกใช้ product['id'], ['name'], ['price']
        # ต้องมั่นใจว่าในตาราง products มี Column เหล่านี้อยู่
        products = conn.execute('SELECT * FROM products').fetchall()
        
        # ดึงข้อมูลหมวดหมู่ (ถ้ามีตาราง categories)
        categories = conn.execute('SELECT * FROM categories').fetchall()
        
        conn.close()
        
        return render_template('index.html', products=products, categories=categories)
    except Exception as e:
        # แสดงข้อผิดพลาดหากเชื่อมต่อฐานข้อมูลไม่ได้
        return f"Database Error: {e}"

if __name__ == '__main__':
    # รันแอปพลิเคชัน
    app.run(debug=True)
