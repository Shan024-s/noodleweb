from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# ระบุ Path ฐานข้อมูลแบบ Full Path เพื่อให้ PythonAnywhere หาเจอ
DB_PATH = '/home/Sun024/noodleweb/noodle.db'

# ตัวแปรจำลองสำหรับเก็บออเดอร์ (ถ้าต้องการถาวรควรสร้างตาราง orders ใน sqlite)
orders_db = []

def get_db_connection():
    """เชื่อมต่อกับ sqlite3"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """แสดงหน้าหลักพร้อมดึงข้อมูลสินค้าจาก Database"""
    try:
        conn = get_db_connection()
        # ดึงสินค้าและหมวดหมู่ไปแสดงใน index.html
        products = conn.execute('SELECT * FROM products').fetchall()
        categories = conn.execute('SELECT * FROM categories').fetchall()
        conn.close()
        return render_template('index.html', products=products, categories=categories)
    except Exception as e:
        return f"Database Error: {e}"

@app.route('/api/order', methods=['POST'])
def place_order():
    try:
        data = request.json
        if not data or 'items' not in data:
            return jsonify({"status": "error", "message": "ข้อมูลไม่ถูกต้อง"}), 400

        new_order = {
            "order_id": len(orders_db) + 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": data['items'],
            "total_price": data['total_price']
        }
        
        orders_db.append(new_order)
        
        print(f"--- New Order Received! ID: {new_order['order_id']} ---")
        return jsonify({
            "status": "success", 
            "message": "ส่งรายการสั่งซื้อเรียบร้อยแล้ว!",
            "order_id": new_order['order_id']
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/orders/history', methods=['GET'])
def get_history():
    return jsonify(orders_db)

if __name__ == '__main__':
    # รันแบบปกติ (บนเครื่องตัวเอง) ไม่ต้องระบุ Port บน PythonAnywhere
    app.run(debug=True)
