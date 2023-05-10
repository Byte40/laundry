import functools
from flask import app, jsonify, request
import mysql.connector

mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="Alexleevex@2",
      database="smart_laundry_db"
)

def handle_bank_link_payment():
    bank_name = request.form['bank_name']
    # Handle bank link payment

def handle_paypal_payment():
    # Handle PayPal payment

def handle_credit_card_payment():
    card_number = request.form['card_number']
    expiry_date = request.form['expiry_date']
    cvv = request.form['cvv']
    # Handle credit card payment

payment_handlers = {
    'bank_link': handle_bank_link_payment,
    'paypal': handle_paypal_payment,
    'credit_card': handle_credit_card_payment
}

@app.route('/place_order', methods=['POST'])
def place_order():
    # Get the customer's information
    customer_name = request.form['customer_name']
    phone_number = request.form['phone_number']
    email = request.form['email']

    # Get the order items
    order_items = request.form.getlist('order_item[]')

    # Calculate the total cost of the order
    total_cost = calculate_total_cost(order_items)

    # Get the payment information
    payment_type = request.form['payment_type']

    # Handle payment
    payment_handler = payment_handlers.get(payment_type)
    if payment_handler is not None:
        payment_handler()

    # Get the locker number
    locker_number = request.form['locker_number']

    # Store the order information in the database
    mycursor = mydb.cursor()
    sql = "INSERT INTO orders (customer_name, phone_number, email, order_items, total_cost, payment_status, locker_number) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (customer_name, phone_number, email, ', '.join(order_items), total_cost, 'paid', locker_number)
    mycursor.execute(sql, val)
    mydb.commit()

    # Return a success message
    return jsonify({'message': 'Order placed successfully'})

def calculate_total_cost(order_items):
    # Calculate the total cost of the order
    total_cost = 0
    for item in order_items:
        # Add the cost of the item to the total cost
        total_cost += get_item_cost(item)

    return total_cost

def get_item_cost(item):
    # Retrieve the cost of an item from the database
    mycursor = mydb.cursor()
    sql = "SELECT cost FROM laundry_items WHERE name = %s"
    val = (item,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()

    return result[0]
