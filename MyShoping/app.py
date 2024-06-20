from flask import Flask, render_template, request, send_file, redirect, url_for
import mysql.connector
import requests
import pandas as pd
from io import BytesIO

app = Flask(__name__)

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="progreso2"
    )

@app.route('/')
def index():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template('products.html', products=products)

@app.route('/order/<int:id>', methods=['POST'])
def order(id):
    quantity = int(request.form['quantity'])
    
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
    product = cursor.fetchone()
    conn.close()

    if not product:
        return "Product not found", 404

    api_url = f'https://rickandmortyapi.com/api/character/{id}'
    response = requests.get(api_url).json()
    product_image = response['image']
    
    data = {
        'ProductID': [product['id']],
        'ProductName': [product['producto']],
        'ProductPrice': [product['precio']],
        'Quantity': [quantity],
        'ProductImage': [product_image]
    }
    df = pd.DataFrame(data)
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    
    return send_file(csv_buffer, mimetype='text/csv', download_name='order.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
