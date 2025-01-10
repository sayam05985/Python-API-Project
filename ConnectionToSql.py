import json  
from datetime import date, datetime
from decimal import Decimal
from http.server import HTTPServer, BaseHTTPRequestHandler
import mysql.connector  



DB_CONF = {
    'host': 'localhost',   
    'user': 'root',        
    'password': 'root',    
    'database': 'Hotel_Python' 
}


def get_db_connection():
    return mysql.connector.connect(**DB_CONF)


def date_converter(obj):
    if isinstance(obj, (datetime, date)):
        return obj.strftime('%Y-%m-%d')
    elif isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Type {type(obj)} not serializable")



class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            if self.path.startswith("/hotels/"):
               
                hotel_id = self.path.split("/")[-1]  
                cursor.execute("SELECT * FROM Hotels WHERE hotel_id = %s", (hotel_id,))
                result = cursor.fetchone()

                if result:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(result, default=date_converter).encode())
                else:
                    self.send_response(404)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Hotel not found"}).encode())

            elif self.path.startswith("/rooms/"):
               
                room_id = self.path.split("/")[-1]
                cursor.execute("SELECT * FROM Rooms WHERE room_id = %s", (room_id,))
                result = cursor.fetchone()

                if result:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(result, default=date_converter).encode())
                else:
                    self.send_response(404)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Room not found"}).encode())

            elif self.path.startswith("/bookings/"):
               
                booking_id = self.path.split("/")[-1]
                cursor.execute("SELECT * FROM Booking WHERE booking_id = %s", (booking_id,))
                result = cursor.fetchone()

                if result:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(result, default=date_converter).encode())
                else:
                    self.send_response(404)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Booking not found"}).encode())

            elif self.path.startswith("/customers/"):
               
                customer_id = self.path.split("/")[-1]
                cursor.execute("SELECT * FROM Customers WHERE customer_id = %s", (customer_id,))
                result = cursor.fetchone()

                if result:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(result, default=date_converter).encode())
                else:
                    self.send_response(404)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Customer not found"}).encode())

            else:
               
                cursor.execute("SELECT * FROM Hotels")
                result = cursor.fetchall()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(result, default=date_converter).encode())

        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")
        
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()


def do_POST(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Parse the POST request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)

            if self.path == "/hotels":
                # Create new hotel
                cursor.execute(
                    "INSERT INTO Hotels (hotel_name, location, rating) VALUES (%s, %s, %s)",
                    (data['hotel_name'], data['location'], data['rating'])
                )
                conn.commit()
                self.send_response(201)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Hotel created successfully"}).encode())

            elif self.path == "/rooms":
                # Create new room
                cursor.execute(
                    "INSERT INTO Rooms (hotel_id, room_type, price, availability) VALUES (%s, %s, %s, %s)",
                    (data['hotel_id'], data['room_type'], data['price'], data['availability'])
                )
                conn.commit()
                self.send_response(201)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Room created successfully"}).encode())

            elif self.path == "/bookings":
                # Create new booking
                cursor.execute(
                    "INSERT INTO Booking (customer_id, room_id, check_in_date, check_out_date, status) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (data['customer_id'], data['room_id'], data['check_in_date'], data['check_out_date'], data['status'])
                )
                conn.commit()
                self.send_response(201)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Booking created successfully"}).encode())

            elif self.path == "/customers":
                # Create new customer
                cursor.execute(
                    "INSERT INTO Customers (first_name, last_name, email, phone) VALUES (%s, %s, %s, %s)",
                    (data['first_name'], data['last_name'], data['email'], data['phone'])
                )
                conn.commit()
                self.send_response(201)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Customer created successfully"}).encode())

            else:
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid endpoint"}).encode())

        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")
        
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


# Start the HTTP server
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()

 # Handle PUT requests (to update resources like hotel, room, booking)
    def do_PUT(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Parse the PUT request body
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(put_data)

            if self.path.startswith("/hotels/"):
                # Update hotel by hotel_id
                hotel_id = self.path.split("/")[-1]
                cursor.execute(
                    "UPDATE Hotels SET hotel_name = %s, location = %s, rating = %s WHERE hotel_id = %s",
                    (data['hotel_name'], data['location'], data['rating'], hotel_id)
                )
                conn.commit()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Hotel updated successfully"}).encode())

            elif self.path.startswith("/rooms/"):
                # Update room by room_id
                room_id = self.path.split("/")[-1]
                cursor.execute(
                    "UPDATE Rooms SET hotel_id = %s, room_type = %s, price = %s, availability = %s WHERE room_id = %s",
                    (data['hotel_id'], data['room_type'], data['price'], data['availability'], room_id)
                )
                conn.commit()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Room updated successfully"}).encode())

            elif self.path.startswith("/bookings/"):
                # Update booking by booking_id
                booking_id = self.path.split("/")[-1]
                cursor.execute(
                    "UPDATE Booking SET customer_id = %s, room_id = %s, check_in_date = %s, "
                    "check_out_date = %s, status = %s WHERE booking_id = %s",
                    (data['customer_id'], data['room_id'], data['check_in_date'], data['check_out_date'], data['status'], booking_id)
                )
                conn.commit()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Booking updated successfully"}).encode())

            elif self.path.startswith("/customers/"):
                # Update customer by customer_id
                customer_id = self.path.split("/")[-1]
                cursor.execute(
                    "UPDATE Customers SET first_name = %s, last_name = %s, email = %s, phone = %s WHERE customer_id = %s",
                    (data['first_name'], data['last_name'], data['email'], data['phone'], customer_id)
                )
                conn.commit()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Customer updated successfully"}).encode())

            else:
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid endpoint"}).encode())

        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")
        
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

# Handle DELETE requests (to delete resources like hotel, room, booking)
    def do_DELETE(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            if self.path.startswith("/hotels/"):
                # Delete hotel by hotel_id
                hotel_id = self.path.split("/")[-1]
                cursor.execute("DELETE FROM Hotels WHERE hotel_id = %s", (hotel_id,))
                conn.commit()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Hotel deleted successfully"}).encode())

            elif self.path.startswith("/rooms/"):
                # Delete room by room_id
                room_id = self.path.split("/")[-1]
                cursor.execute("DELETE FROM Rooms WHERE room_id = %s", (room_id,))
                conn.commit()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Room deleted successfully"}).encode())

            elif self.path.startswith("/bookings/"):
                # Delete booking by booking_id
                booking_id = self.path.split("/")[-1]
                cursor.execute("DELETE FROM Booking WHERE booking_id = %s", (booking_id,))
                conn.commit()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Booking deleted successfully"}).encode())

            elif self.path.startswith("/customers/"):
                # Delete customer by customer_id
                customer_id = self.path.split("/")[-1]
                cursor.execute("DELETE FROM Customers WHERE customer_id = %s", (customer_id,))
                conn.commit()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Customer deleted successfully"}).encode())

            else:
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid endpoint"}).encode())

        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


# Server setup to run on port 8000
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()


# Start the server when the script is executed
if __name__ == "__main__":
    run()


def do_GET(self):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if self.path.startswith("/rooms/check-availability"):
            # Check Room Availability
            query_params = self.path.split("?")[-1]
            params = dict(param.split("=") for param in query_params.split("&"))
            room_id = params.get("room_id")
            check_in_date = params.get("check_in_date")
            check_out_date = params.get("check_out_date")

            cursor.execute(
                """
                SELECT check_room_availability(%s, %s, %s) AS availability
                """,
                (room_id, check_in_date, check_out_date)
            )
            result = cursor.fetchone()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result, default=date_converter).encode())

        elif self.path.startswith("/rooms"):
            # Fetch all rooms
            cursor.execute("SELECT * FROM Rooms")
            result = cursor.fetchall()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result, default=date_converter).encode())

        else:
            self.send_error(404, "Endpoint not found")

    except Exception as e:
        self.send_error(500, f"Server error: {str(e)}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def do_POST(self):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if self.path == "/bookings":
            # Create a new booking
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))

            cursor.execute(
                """
                INSERT INTO Booking (customer_id, room_id, check_in_date, check_out_date, status)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    post_data['customer_id'],
                    post_data['room_id'],
                    post_data['check_in_date'],
                    post_data['check_out_date'],
                    post_data['status']
                )
            )
            conn.commit()

            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Booking created successfully"}).encode())

        else:
            self.send_error(404, "Endpoint not found")

    except mysql.connector.Error as e:
        if e.errno == 20001:  # Trigger exception for double booking
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_error(500, f"Database error: {str(e)}")

    except Exception as e:
        self.send_error(500, f"Server error: {str(e)}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def do_DELETE(self):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if self.path.startswith("/bookings/"):
            booking_id = self.path.split("/")[-1]

            cursor.execute(
                "DELETE FROM Booking WHERE booking_id = %s",
                (booking_id,)
            )
            conn.commit()

            if cursor.rowcount > 0:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Booking deleted successfully"}).encode())
            else:
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Booking not found"}).encode())

        else:
            self.send_error(404, "Endpoint not found")

    except Exception as e:
        self.send_error(500, f"Server error: {str(e)}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()