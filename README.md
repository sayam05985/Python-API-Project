Name:- Sayam Balasahe Godase
Gmail:- sayamgodase@gmail.com
Class:- TE-A

# Hotel Reservation System API

## Overview
This project implements a Python-based REST API for managing a hotel reservation system. The API allows users to perform CRUD (Create, Read, Update, Delete) operations on hotels, rooms, bookings, and customers. It uses MySQL as the database backend and supports operations like checking room availability and managing reservations.

## Features
- **Hotels**: Add, retrieve, update, and delete hotel details.
- **Rooms**: Manage rooms for hotels with their type, price, and availability status.
- **Bookings**: Create, retrieve, update, and cancel bookings.
- **Customers**: Manage customer details such as name, email, and phone.
- **Room Availability**: Check the availability of rooms for a given date range.

## Prerequisites
Before running the application, ensure the following are installed:
- Python 3.8 or later
- MySQL server
- Postman or any HTTP client (for API testing)

## Database Setup
1. Create a MySQL database named `hotel`.
2. Execute the provided SQL script to create the necessary tables:
   ```sql
   CREATE TABLE Hotels (
       hotel_id INT PRIMARY KEY AUTO_INCREMENT,
       hotel_name VARCHAR(100),
       location VARCHAR(100),
       rating INT CHECK (rating BETWEEN 1 AND 5)
   );

   CREATE TABLE Rooms (
       room_id INT PRIMARY KEY AUTO_INCREMENT,
       hotel_id INT,
       room_type VARCHAR(50),
       price DECIMAL(10, 2) CHECK (price > 0),
       availability CHAR(1) CHECK (availability IN ('Y', 'N')),
       FOREIGN KEY (hotel_id) REFERENCES Hotels(hotel_id)
   );

   CREATE TABLE Customers (
       customer_id INT PRIMARY KEY AUTO_INCREMENT,
       first_name VARCHAR(50),
       last_name VARCHAR(50),
       email VARCHAR(100) UNIQUE,
       phone VARCHAR(15) UNIQUE
   );

   CREATE TABLE Booking (
       booking_id INT PRIMARY KEY AUTO_INCREMENT,
       customer_id INT,
       room_id INT,
       check_in_date DATE,
       check_out_date DATE,
       status VARCHAR(20) CHECK (status IN ('Confirmed', 'Cancelled')),
       FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
       FOREIGN KEY (room_id) REFERENCES Rooms(room_id)
   );
   ```

3. Add your database credentials to the `DB_CONF` dictionary in the code:
   ```python
   DB_CONF = {
       'host': 'localhost',
       'user': 'root',
       'password': 'your_password',
       'database': 'hotel'
   }
   ```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/hotel-reservation-api.git
   cd hotel-reservation-api
   ```

2. Install the required dependencies:
   ```bash
   pip install mysql-connector-python
   ```

3. Run the server:
   ```bash
   python app.py
   ```

4. The server will start on `http://localhost:8000`.

## API Endpoints
### Hotels
- **GET** `/hotels`: Get all hotels.
- **GET** `/hotels/{hotel_id}`: Get details of a specific hotel.
- **POST** `/hotels`: Add a new hotel.
  ```json
  {
      "hotel_name": "Hotel Paradise",
      "location": "Hawaii",
      "rating": 5
  }
  ```
- **PUT** `/hotels/{hotel_id}`: Update hotel details.
- **DELETE** `/hotels/{hotel_id}`: Delete a hotel.

### Rooms
- **GET** `/rooms`: Get all rooms.
- **POST** `/rooms`: Add a new room.
- **PUT** `/rooms/{room_id}`: Update room details.
- **DELETE** `/rooms/{room_id}`: Delete a room.

### Bookings
- **GET** `/bookings`: Get all bookings.
- **POST** `/bookings`: Add a new booking.
  ```json
  {
      "customer_id": 1,
      "room_id": 2,
      "check_in_date": "2025-01-10",
      "check_out_date": "2025-01-15",
      "status": "Confirmed"
  }
  ```
- **PUT** `/bookings/{booking_id}`: Update booking details.
- **DELETE** `/bookings/{booking_id}`: Cancel a booking.

### Customers
- **GET** `/customers`: Get all customers.
- **POST** `/customers`: Add a new customer.
- **PUT** `/customers/{customer_id}`: Update customer details.
- **DELETE** `/customers/{customer_id}`: Delete a customer.

Testing with Postman
1. Open Postman and create a new collection.
2. Add requests for the endpoints listed above.
3. Test the API by sending requests and observing the responses.





