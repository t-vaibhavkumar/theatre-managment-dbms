import streamlit as st
import sqlite3
import os
from datetime import datetime

# Initialize the database
def init_db():
    conn = sqlite3.connect('theater.db')
    cursor = conn.cursor()

    # Create tables based on your ER model
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY,
            email TEXT,
            password TEXT,
            name TEXT,
            phone_number TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Movies (
            movie_id INTEGER PRIMARY KEY,
            name TEXT,
            language TEXT,
            genre TEXT,
            release_date TEXT,
            rating REAL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Shows (
            show_id INTEGER PRIMARY KEY,
            screen_id INTEGER,
            movie_id INTEGER,
            show_time TEXT,
            date TEXT,
            FOREIGN KEY (movie_id) REFERENCES Movies(movie_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Bookings (
            booking_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            show_id INTEGER,
            seats INTEGER,
            payment_status TEXT,
            FOREIGN KEY (user_id) REFERENCES Users(user_id),
            FOREIGN KEY (show_id) REFERENCES Shows(show_id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Run the initialization
if not os.path.exists('theater.db'):
    init_db()

# Function to fetch movies from the database
def get_movies():
    conn = sqlite3.connect('theater.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Movies")
    movies = cursor.fetchall()
    conn.close()
    return movies

# Function to add a new movie
def add_movie(name, language, genre, release_date, rating):
    conn = sqlite3.connect('theater.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Movies (name, language, genre, release_date, rating) VALUES (?, ?, ?, ?, ?)",
                   (name, language, genre, release_date, rating))
    conn.commit()
    conn.close()

# Function to book tickets
def book_tickets(user_id, show_id, seats, payment_status):
    conn = sqlite3.connect('theater.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Bookings (user_id, show_id, seats, payment_status) VALUES (?, ?, ?, ?)",
                   (user_id, show_id, seats, payment_status))
    conn.commit()
    conn.close()

# Streamlit Interface
st.title("Theater Management System")

# Display available movies
st.header("Available Movies")
movies = get_movies()
for movie in movies:
    st.write(f"Name: {movie[1]}, Language: {movie[2]}, Genre: {movie[3]}, Release Date: {movie[4]}, Rating: {movie[5]}/5")

# Form to add a new movie
st.header("Add a New Movie")
with st.form("add_movie_form"):
    movie_name = st.text_input("Movie Name")
    movie_language = st.text_input("Language")
    movie_genre = st.text_input("Genre")
    movie_release_date = st.date_input("Release Date")
    movie_rating = st.slider("Rating", 0.0, 5.0, step=0.1)
    submitted = st.form_submit_button("Add Movie")
    if submitted:
        add_movie(movie_name, movie_language, movie_genre, movie_release_date.strftime("%Y-%m-%d"), movie_rating)
        st.success(f"Movie '{movie_name}' added successfully!")

# Form to book tickets
st.header("Book Tickets")
with st.form("book_tickets_form"):
    user_id = st.number_input("User ID", min_value=1)
    show_id = st.number_input("Show ID", min_value=1)
    seats = st.number_input("Number of Seats", min_value=1)
    payment_status = st.selectbox("Payment Status", ["Pending", "Paid"])
    booking_submitted = st.form_submit_button("Book Tickets")
    if booking_submitted:
        book_tickets(user_id, show_id, seats, payment_status)
        st.success(f"Tickets booked successfully for Show ID {show_id}!")

