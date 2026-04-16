from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

orders_db = []

@app.route('/')
def index():
    return render_template('index.html')

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
        for item in new_order['items']:
            print(f"- {item['name']} ({item['detail']}) : {item['price']} ฿")
        print(f"Total: {new_order['total_price']} ฿")

        return jsonify({
            "status": "success", 
            "message": "ส่งรายการสั่งซื้อเรียบร้อยแล้ว!",
            "order_id": new_order['order_id']
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# @app.route('/api/orders/history', methods=['GET'])
# def get_history():
#     return jsonify(orders_db)

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
