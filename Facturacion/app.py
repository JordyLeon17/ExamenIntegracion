from flask import Flask, request, jsonify, render_template
import mysql.connector
from datetime import datetime

app = Flask(__name__)

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="inventario"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_invoice', methods=['POST'])
def add_invoice():
    order_id = request.json.get('order_id')
    
    if not order_id:
        return jsonify({"error": "order_id is required"}), 400

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    
    # Verificar si la orden existe
    cursor.execute("SELECT * FROM ordenes WHERE id = %s", (order_id,))
    order = cursor.fetchone()
    
    if not order:
        return jsonify({"error": "Order not found"}), 404
    
    product_id = order['product_id']
    quantity = order['quantity']
    
    # Obtener el precio del producto
    cursor.execute("SELECT price FROM productos WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    product_price = product['price']
    
    # Calcular el total
    total = product_price * quantity
    invoice_date = datetime.now().strftime('%Y-%m-%d')
    
    # Insertar la factura
    cursor.execute("INSERT INTO facturas (order_id, fecha, total) VALUES (%s, %s, %s)", 
                   (order_id, invoice_date, total))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Factura ingresada con éxito"}), 201

if __name__ == '__main__':
    app.run(debug=True)
