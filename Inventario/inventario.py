import mysql.connector
import pandas as pd
from datetime import datetime
import os

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="inventario"
    )

def update_inventory_from_csv(csv_file):

    # Obtener la ruta del archivo CSV relativo al script
    csv_path = os.path.join(os.path.dirname(__file__), csv_file)

    # Leer el CSV
    df = pd.read_csv(csv_path)
    
    # Conectar a la base de datos
    conn = connect_db()
    cursor = conn.cursor()
    
    for index, row in df.iterrows():
        product_id = row['ProductID']
        quantity = row['Quantity']
        product_name = row['ProductName']
        product_price = row['ProductPrice']
        product_image = row['ProductImage']
        
        # Actualizar stock del producto
        cursor.execute("SELECT stock FROM productos WHERE id = %s", (product_id,))
        result = cursor.fetchone()
        if result:
            new_stock = result[0] - quantity
            cursor.execute("UPDATE productos SET stock = %s WHERE id = %s", (new_stock, product_id))
        else:
            cursor.execute("INSERT INTO productos (id, product_name, price, stock) VALUES (%s, %s, %s, %s)",
                           (product_id, product_name, product_price, -quantity))
        
        # Insertar orden de compra
        cursor.execute("INSERT INTO ordenes (product_id, quantity, product_image) VALUES (%s, %s, %s)",
                       (product_id, quantity, product_image))
        order_id = cursor.lastrowid
        
    
    # Confirmar cambios
    conn.commit()
    cursor.close()
    conn.close()

# Llamar a la función con el archivo CSV generado anteriormente
update_inventory_from_csv('order.csv')