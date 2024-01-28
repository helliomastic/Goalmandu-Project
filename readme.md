# Goal Mandu

## Introduction
Welcome to the documentation for the Futsal Booking System! This system is designed to streamline the process of booking futsal courts and managing reservations.

## Technologies Used

### Backend

- **Flask:** A lightweight Python web framework.
- **SQLAlchemy:** An SQL toolkit and Object-Relational Mapping (ORM) library.
- **SQLite:** A lightweight database engine for easy deployment.

### Frontend

- **HTML, CSS, and JavaScript:** Standard web technologies for building user interfaces.
- **Bootstrap:** A front-end framework for responsive design.
- **Jinja2:** A templating engine for integrating Python code into HTML templates.

### Authentication

- **Flask-Login:** Handles user authentication and session management.



## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/prajwalbasnet4400/goalmandu.git
    ```

2. Navigate to the project directory:

    ```bash
    cd goalmandu
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:

    ```bash
    flask run
    ```

2. Open your browser and navigate to [http://localhost:5000](http://localhost:5000).



## Features

### 1. User Authentication

- Secure user registration and login.

### 2. Futsal Court Booking

- Browse available futsal courts.
- Reserve a court for a specific date and time.

### 3. Booking Management

- View and manage your booked futsal courts.
- Cancel or modify existing reservations.

### 4. Administrator Dashboard

- Admin-only access for managing users and bookings.
- View and modify any booking or user account.

### 5. Futsal Dashboard

- Futsal Staff-only access for managing bookings.
- View , add and cancel bookings


## Database Schema

### Users Table

- `id`: User ID (integer, primary key)
- `name`: User's username (string, unique)
- `phone`: User's phone no (string, unique)
- `password`: User's hashed password (string)
- `type`: User's type(User,Staff,Admin)

### Bookings Table

- `id`: Booking ID (integer, primary key)
- `user_id`: ID of the user who made the booking (integer, foreign key to Users table)
- `futsal_id`: ID of the booked futsal court (integer, foreign key to Courts table)
- `date`: Booking date (date)
- `time`: Booking time (time)
- `status`: Booking status (string, e.g., confirmed, pending, canceled)
- `cost`: Cost of futsal booking (float)

### Futsals Table

- `id`: Futsal ID (integer, primary key)
- `name`: Futsal name (string)
- `location`: Futsal location (string)
- `contacts`: Contact Info (string)

