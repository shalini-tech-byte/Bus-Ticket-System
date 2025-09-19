# app.py
from flask import Flask, render_template, request
import mysql.connector
from db_config import get_db_connection

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['POST'])
def book_ticket():
    full_name = request.form['full_name']
    email = request.form['email']
    phone_number = request.form['phone_number']
    schedule_id = int(request.form['schedule_id'])
    seat_number = int(request.form['seat_number'])

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1. Insert passenger
        cursor.execute("""
            INSERT INTO passengers (full_name, email, phone_number)
            VALUES (%s, %s, %s)
        """, (full_name, email, phone_number))
        passenger_id = cursor.lastrowid

        # 2. Insert booking
        cursor.execute("""
            INSERT INTO bookings (schedule_id, passenger_id, seat_number)
            VALUES (%s, %s, %s)
        """, (schedule_id, passenger_id, seat_number))

        conn.commit()
        return f"<h3>Booking Successful!</h3><p>Passenger ID: {passenger_id}</p>"
    except mysql.connector.Error as err:
        conn.rollback()
        return f"<h3>Booking Failed:</h3><p>{err}</p>"
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
