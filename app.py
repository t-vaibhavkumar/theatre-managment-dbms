import streamlit as st
import sqlite3
from datetime import datetime

# Database connection
def create_connection():
    return sqlite3.connect("theatre_management.db")

# Initialize the database and tables
def create_tables():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Customer (
                        User_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Name TEXT,
                        Email TEXT,
                        Password TEXT,
                        Phone_Number TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Movie (
                        Movie_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Name TEXT,
                        Language TEXT,
                        Genre TEXT,
                        Release_Date TEXT,
                        Rating REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Booking (
                        Booking_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        User_ID INTEGER,
                        Movie_ID INTEGER,
                        Screen_ID INTEGER,
                        Booking_Date TEXT,
                        Number_of_Seats INTEGER,
                        FOREIGN KEY (User_ID) REFERENCES Customer(User_ID),
                        FOREIGN KEY (Movie_ID) REFERENCES Movie(Movie_ID))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Payment (
                        Payment_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Booking_ID INTEGER,
                        Amount REAL,
                        Payment_Type TEXT,
                        Payment_Status TEXT,
                        FOREIGN KEY (Booking_ID) REFERENCES Booking(Booking_ID))''')
    connection.commit()
    cursor.close()
    connection.close()

# Home Page: Display available movies
def show_movies():
    st.header("Available Movies")
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT Name, Language, Genre, Release_Date, Rating FROM Movie")
    movies = cursor.fetchall()
    cursor.close()
    connection.close()

    if movies:
        for movie in movies:
            st.write(f"**Title:** {movie[0]}, **Language:** {movie[1]}, **Genre:** {movie[2]}, **Release Date:** {movie[3]}, **Rating:** {movie[4]}")
    else:
        st.write("No movies available.")

# Register a new customer
def register_customer():
    st.header("Customer Registration")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    phone = st.text_input("Phone Number")

    if st.button("Register"):
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Customer (Name, Email, Password, Phone_Number) VALUES (?, ?, ?, ?)", 
                       (name, email, password, phone))
        connection.commit()
        cursor.close()
        connection.close()
        st.success("Registration successful!")

# Book a ticket
def book_ticket():
    st.header("Book a Ticket")
    user_id = st.number_input("User ID", min_value=1, step=1)
    movie_id = st.number_input("Movie ID", min_value=1, step=1)
    screen_id = st.number_input("Screen ID", min_value=1, step=1)
    seats = st.number_input("Number of Seats", min_value=1, step=1)

    if st.button("Confirm Booking"):
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Booking (User_ID, Movie_ID, Screen_ID, Booking_Date, Number_of_Seats) VALUES (?, ?, ?, ?, ?)",
                       (user_id, movie_id, screen_id, datetime.now().strftime("%Y-%m-%d"), seats))
        connection.commit()
        cursor.close()
        connection.close()
        st.success("Booking confirmed!")

# Process a payment
def process_payment():
    st.header("Payment")
    booking_id = st.number_input("Booking ID", min_value=1, step=1)
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    payment_type = st.selectbox("Payment Type", ["Credit Card", "Debit Card", "UPI", "Net Banking"])

    if st.button("Make Payment"):
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Payment (Booking_ID, Amount, Payment_Type, Payment_Status) VALUES (?, ?, ?, ?)", 
                       (booking_id, amount, payment_type, "Completed"))
        connection.commit()
        cursor.close()
        connection.close()
        st.success("Payment successful!")

# Sidebar navigation
st.sidebar.title("Theatre Management System")
page = st.sidebar.radio("Go to", ["Home", "Register", "Book Ticket", "Payment"])

# Page routing
create_tables()  # Ensure tables are created
if page == "Home":
    show_movies()
elif page == "Register":
    register_customer()
elif page == "Book Ticket":
    book_ticket()
elif page == "Payment":
    process_payment()
