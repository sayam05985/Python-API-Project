-- HOTEL RESERVATION SYSTEM

-- Create Hotels Table
CREATE TABLE Hotels (
    hotel_id NUMBER PRIMARY KEY,
    hotel_name VARCHAR2(100),
    location VARCHAR2(100),
    rating NUMBER CHECK (rating BETWEEN 1 AND 5) 
);

-- Create Rooms Table
CREATE TABLE Rooms (
    room_id NUMBER PRIMARY KEY,
    hotel_id NUMBER REFERENCES Hotels(hotel_id),
    room_type VARCHAR2(50),
    price NUMBER CHECK (price > 0),
    availability CHAR(1) CHECK (availability IN ('Y', 'N')) 
);

-- Create Customers Table
CREATE TABLE Customers (
    customer_id NUMBER PRIMARY KEY,
    first_name VARCHAR2(50),
    last_name VARCHAR2(50),
    email VARCHAR2(100) UNIQUE, 
    phone VARCHAR2(15) UNIQUE 
);

-- Create Bookings Table
CREATE TABLE Booking (
    booking_id NUMBER PRIMARY KEY,
    customer_id NUMBER REFERENCES Customers(customer_id),
    room_id NUMBER REFERENCES Rooms(room_id),
    check_in_date DATE,
    check_out_date DATE,
    status VARCHAR2(20) CHECK (status IN ('Confirmed', 'Cancelled')),
    CONSTRAINT chk_booking_dates CHECK (check_in_date < check_out_date) 
);

-- Add Feedback Table for Customer Reviews
CREATE TABLE Feedback (
    feedback_id NUMBER PRIMARY KEY,
    booking_id NUMBER REFERENCES Booking(booking_id),
    rating NUMBER CHECK (rating BETWEEN 1 AND 5),
    comments VARCHAR2(500)
);

-- Check Room Availability
CREATE OR REPLACE FUNCTION check_room_availability(
    p_room_id IN NUMBER,
    p_check_in_date IN DATE,
    p_check_out_date IN DATE
) RETURN CHAR IS
    v_count NUMBER;
BEGIN
    SELECT COUNT(*)
    INTO v_count
    FROM Booking
    WHERE room_id = p_room_id
      AND status = 'Confirmed'
      AND (
          (check_in_date < p_check_out_date AND check_out_date > p_check_in_date)
      );

    IF v_count > 0 THEN
        RETURN 'N'; -- Not available
    ELSE
        RETURN 'Y'; -- Available
    END IF;
END check_room_availability;
/

-- Trigger to Prevent Double Bookings
CREATE OR REPLACE TRIGGER prevent_double_booking
BEFORE INSERT ON Booking
FOR EACH ROW
DECLARE
    v_availability CHAR(1);
BEGIN
    v_availability := check_room_availability(:NEW.room_id, :NEW.check_in_date, :NEW.check_out_date);
    
    IF v_availability = 'N' THEN
        RAISE_APPLICATION_ERROR(-20001, 'Room is already booked for the selected dates.');
    END IF;
END;
/

-- Generate the Report on Occupancy Rate
SELECT 
    h.hotel_name,
    COUNT(b.booking_id) AS total_bookings,
    COUNT(r.room_id) AS total_rooms,
    CASE 
        WHEN COUNT(r.room_id) = 0 THEN 0
        ELSE (COUNT(b.booking_id) / COUNT(r.room_id)) * 100 
    END AS occupancy_rate
FROM 
    Hotels h
LEFT JOIN 
    Rooms r ON h.hotel_id = r.hotel_id
LEFT JOIN 
    Booking b ON r.room_id = b.room_id AND b.status = 'Confirmed'
GROUP BY 
    h.hotel_name;


    
-- Insert Sample Records in the Tables to Show the Output

-- Insert Sample Hotels
INSERT INTO Hotels (hotel_id, hotel_name, location, rating) 
VALUES (1, 'Hotel California', 'California', 5);
INSERT INTO Hotels (hotel_id, hotel_name, location, rating) 
VALUES (2, 'Grand Hotel', 'New York', 4);
INSERT INTO Hotels (hotel_id, hotel_name, location, rating) 
VALUES (3, 'Paradise Inn', 'Florida', 5);
INSERT INTO Hotels (hotel_id, hotel_name, location, rating) 
VALUES (4, 'Ocean View', 'Hawaii', 4);
INSERT INTO Hotels (hotel_id, hotel_name, location, rating) 
VALUES (5, 'Mountain Retreat', 'Colorado', 3);
INSERT INTO Hotels (hotel_id, hotel_name, location, rating) 
VALUES (6, 'City Center', 'Chicago', 4);
INSERT INTO Hotels (hotel_id, hotel_name, location, rating) 
VALUES (7, 'Luxury Stay', 'Las Vegas', 5);
INSERT INTO Hotels (hotel_id, hotel_name, location, rating) 
VALUES (8, 'Sunset Lodge', 'Texas', 3);
INSERT INTO Hotels (hotel_id, hotel_name, location, rating) 
VALUES (9, 'The Royal', 'Washington', 5);
INSERT INTO Hotels (hotel_id, hotel_name, location, rating) 
VALUES (10, 'Forest Cabin', 'Oregon', 4);
INSERT INTO Hotels (hotel_id, hotel_name, location, rating) 
VALUES (11, 'Beach Resort', 'Miami', 5);
INSERT INTO Hotels (hotel_id, hotel_name, location, rating) 
VALUES (12, 'Downtown Suites', 'San Francisco', 4);
INSERT INTO Hotels (hotel_id, hotel_name, location, rating) 
VALUES (13, 'Hilltop Hotel', 'Arizona', 3);
INSERT INTO Hotels (hotel_id, hotel_name, location, rating) 
VALUES (14, 'Desert Haven', 'Nevada', 5);
INSERT INTO Hotels (hotel_id, hotel_name, location, rating) 
VALUES (15, 'Crystal Palace', 'New Jersey', 4);

-- Insert Sample Rooms
INSERT INTO Rooms (room_id, hotel_id, room_type, price, availability) 
VALUES (1, 1, 'Single', 100, 'Y');
INSERT INTO Rooms (room_id, hotel_id, room_type, price, availability) 
VALUES (2, 1, 'Double', 150, 'Y');
INSERT INTO Rooms (room_id, hotel_id, room_type, price, availability) 
VALUES (3, 2, 'Suite', 200, 'Y');
INSERT INTO Rooms (room_id, hotel_id, room_type, price, availability) 
VALUES (4, 3, 'Single', 90, 'Y');
INSERT INTO Rooms (room_id, hotel_id, room_type, price, availability) 
VALUES (5, 4, 'Double', 180, 'Y');
INSERT INTO Rooms (room_id, hotel_id, room_type, price, availability) 
VALUES (6, 5, 'Suite', 250, 'Y');
INSERT INTO Rooms (room_id, hotel_id, room_type, price, availability) 
VALUES (7, 6, 'Single', 120, 'Y');
INSERT INTO Rooms (room_id, hotel_id, room_type, price, availability) 
VALUES (8, 7, 'Double', 160, 'Y');
INSERT INTO Rooms (room_id, hotel_id, room_type, price, availability) 
VALUES (9, 8, 'Suite', 300, 'Y');
INSERT INTO Rooms (room_id, hotel_id, room_type, price, availability) 
VALUES (10, 9, 'Single', 110, 'Y');
INSERT INTO Rooms (room_id, hotel_id, room_type, price, availability) 
VALUES (11, 10, 'Double', 140, 'Y');
INSERT INTO Rooms (room_id, hotel_id, room_type, price, availability) 
VALUES (12, 11, 'Suite', 220, 'Y');
INSERT INTO Rooms (room_id, hotel_id, room_type, price, availability) 
VALUES (13, 12, 'Single', 100, 'Y');
INSERT INTO Rooms (room_id, hotel_id, room_type, price, availability) 
VALUES (14, 13, 'Double', 170, 'Y');
INSERT INTO Rooms (room_id, hotel_id, room_type, price, availability) 
VALUES (15, 14, 'Suite', 270, 'Y');

-- Insert Sample Customers
INSERT INTO Customers (customer_id, first_name, last_name, email, phone) 
VALUES (1, 'John', 'Doe', 'john.doe@example.com', '123456');
INSERT INTO Customers (customer_id, first_name, last_name, email, phone) 
VALUES (2, 'Jane', 'Smith', 'jane.smith@example.com', '234567');
INSERT INTO Customers (customer_id, first_name, last_name, email, phone) 
VALUES (3, 'Michael', 'Brown', 'michael.brown@example.com', '345678');
INSERT INTO Customers (customer_id, first_name, last_name, email, phone) 
VALUES (4, 'Emily', 'Johnson', 'emily.johnson@example.com', '456789');
INSERT INTO Customers (customer_id, first_name, last_name, email, phone) 
VALUES (5, 'Chris', 'Davis', 'chris.davis@example.com', '567890');
INSERT INTO Customers (customer_id, first_name, last_name, email, phone) 
VALUES (6, 'Sarah', 'Lee', 'sarah.lee@example.com', '678901');
INSERT INTO Customers (customer_id, first_name, last_name, email, phone) 
VALUES (7, 'Daniel', 'Martinez', 'daniel.martinez@example.com', '789')

-- Test the function and triggers with sample data

INSERT INTO Booking (booking_id, customer_id, room_id, check_in_date, check_out_date, status) 
VALUES (1, 1, 1, TO_DATE('2025-01-10', 'YYYY-MM-DD'), TO_DATE('2025-01-15', 'YYYY-MM-DD'), 'Confirmed');

-- Check room availability
SELECT check_room_availability(1, TO_DATE('2025-01-12', 'YYYY-MM-DD'), TO_DATE('2025-01-16', 'YYYY-MM-DD')) FROM DUAL;

