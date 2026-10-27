# 🏔️ Adventure Trip Management System

A **console-based Adventure Trip Management System** developed using **Python** and **Object-Oriented Programming (OOP)** concepts, with **MongoDB Atlas** used for persistent data storage.

The system provides a simple command-line interface for managing customers, adventure trips, guides, bookings, payments, and booking cancellations.

---

## 📌 Project Overview

The **Adventure Trip Management System** is a Python-based console application designed to manage adventure trip bookings.

Users can:

- Register customers
- View available adventure trips
- Select an adventure trip
- Select the number of persons
- Select a guide
- Calculate the total booking cost
- Complete payment through the console
- Store customer information in MongoDB Atlas
- Store booking information in MongoDB Atlas
- View bookings
- Cancel bookings

The main objective of this project is to apply **Python OOP concepts** to a practical real-world application.

---

## 🚀 Features

### 👤 Customer Management

- Customer registration
- Automatic customer ID generation
- Customer name validation
- 10-digit mobile number validation
- Email validation
- Duplicate mobile number checking
- Duplicate email checking
- Customer details display

### 🏕️ Adventure Trips

The system provides different adventure activities:

- Trekking
- Rafting
- Camping

Each trip contains:

- Trip ID
- Trip name
- Location
- Duration
- Base price

Each type of trip has its own cost calculation method.

### 🧑‍🏫 Guide Management

Guides can be assigned according to the selected adventure activity.

Each guide contains:

- Guide ID
- Guide name
- Specialization

### 📋 Booking Management

The booking module allows users to:

- Select a trip
- Select number of persons
- Select a guide
- Calculate total cost
- Confirm booking
- Store booking information
- View booking details
- Cancel bookings

### 💳 Payment Management

The project includes a simple **console-based payment system**.

Available options:

```text
1. Cash Payment
2. Cancel Payment
```

The payment status is stored along with the booking information.

---

## 🗄️ MongoDB Atlas

The project uses **MongoDB Atlas** for persistent data storage.

Database:

```text
adventure_trip
```

Collections:

```text
customers
bookings
```

### Customers Collection

Stores customer information such as:

- Customer ID
- Name
- Mobile number
- Email

### Bookings Collection

Stores booking information such as:

- Booking ID
- Customer ID
- Trip ID
- Trip name
- Number of persons
- Guide name
- Total cost
- Payment ID
- Booking status

---

## 🧠 OOP Concepts Used

This project demonstrates important **Object-Oriented Programming concepts in Python**.

### 1. Classes and Objects

The project contains classes such as:

```text
AdventureTrip
TrekkingTrip
RaftingTrip
CampingTrip
Customer
Guide
Booking
Payment
```

Objects are created from these classes to manage different parts of the application.

### 2. Inheritance

The trip classes inherit from the base `AdventureTrip` class.

```text
AdventureTrip
      │
      ├── TrekkingTrip
      ├── RaftingTrip
      └── CampingTrip
```

### 3. Abstraction

`AdventureTrip` is an abstract base class using Python's:

```python
ABC
abstractmethod
```

The `calculate_cost()` method is defined as an abstract method and implemented by child classes.

### 4. Polymorphism

Different trip classes implement their own version of:

```python
calculate_cost()
```

Therefore, the same method can produce different results depending on the selected trip.

### 5. Encapsulation

Related data and methods are organized inside their respective classes.

For example, customer-related information is managed through the `Customer` class, while booking-related information is managed through the `Booking` class.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Python OOP | Application architecture |
| MongoDB Atlas | Database |
| PyMongo | MongoDB connectivity |
| Flask | Local application support, if included |
| python-dotenv | Environment variable management |
| Regular Expressions | Input validation |
| Git | Version control |
| GitHub | Project hosting |

---

## 📁 Project Structure

```text
Adventure_TripManagement_System/
│
├── main.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── .env
```

### File Description

#### `main.py`

Contains the main application logic, OOP classes, menu system, customer registration, trip selection, booking management, validation, and payment handling.

#### `database.py`

Handles the MongoDB Atlas connection and database operations.

It provides functionality for:

- Adding customers
- Finding customers
- Checking duplicate mobile/email
- Adding bookings
- Retrieving bookings
- Cancelling bookings

#### `requirements.txt`

Contains the Python packages required to run the project.

#### `.env`

Stores private environment variables such as the MongoDB Atlas connection string.

The `.env` file is excluded from GitHub using `.gitignore`.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Kunal173178/Python-project.git
```

### 2. Open the Project

```bash
cd Python-project/Adventure_TripManagement_System
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file inside the project folder.

Add your MongoDB Atlas connection string:

```env
MONGODB_URI=your_mongodb_atlas_connection_string
```

Example format:

```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
```

> Replace the username, password and cluster information with your own MongoDB Atlas credentials.

### 🔒 Security

**Never upload `.env` to GitHub.**

The project uses `.gitignore` to prevent private credentials from being committed.

---

## 🗄️ MongoDB Atlas Setup

To connect the project with MongoDB Atlas:

1. Create a MongoDB Atlas account.
2. Create a cluster.
3. Create a database user.
4. Configure Network Access.
5. Copy the MongoDB connection string.
6. Add the connection string to `.env`.
7. Run the application.

The application connects to:

```text
Database: adventure_trip
```

Collections:

```text
customers
bookings
```

---

## ▶️ Run the Project

From the project directory:

```bash
python main.py
```

The application runs completely through the **console/terminal**.

Example:

```text
========================================
     ADVENTURE TRIP MANAGEMENT SYSTEM
========================================

1. Register Customer
2. View Trips
3. Create Booking
4. View Bookings
5. Cancel Booking
6. Exit
```

---

## 🔄 Application Flow

```text
Start Application
       │
       ▼
Connect to MongoDB Atlas
       │
       ▼
Customer Registration
       │
       ▼
View Adventure Trips
       │
       ▼
Select Trip
       │
       ▼
Select Number of Persons
       │
       ▼
Select Guide
       │
       ▼
Calculate Total Cost
       │
       ▼
Confirm Booking
       │
       ▼
Payment
       │
       ▼
Booking Created
       │
       ▼
Save Booking in MongoDB
```

---

## 💰 Cost Calculation

Different adventure trips use different cost calculation rules.

### Trekking

```text
Total Cost = Trip Price × Persons + Guide Charge
```

### Rafting

```text
Total Cost = Trip Price × Persons + Equipment Charge
```

### Camping

```text
Total Cost = Trip Price × Persons + Camping Charge
```

This demonstrates **polymorphism**, because each trip class provides its own implementation of `calculate_cost()`.

---

## ✅ Input Validation

The system validates important user inputs including:

- Customer name
- Mobile number
- Email address
- Number of persons
- Payment selection
- Duplicate customer information

Invalid input is rejected and the user is asked to enter the information again.

---

## 🗃️ Database Design

### Customers

```text
customers
│
├── _id
├── name
├── mobile
└── email
```

### Bookings

```text
bookings
│
├── _id
├── customer_id
├── trip_id
├── trip_name
├── persons
├── guide_name
├── total_cost
├── payment_id
└── status
```

---

## 🎯 Learning Objectives

This project helped in practicing:

- Python programming
- Object-Oriented Programming
- Classes and Objects
- Inheritance
- Abstraction
- Polymorphism
- Encapsulation
- Abstract Classes
- Exception Handling
- Input Validation
- Regular Expressions
- MongoDB
- PyMongo
- Environment Variables
- Git and GitHub

---

## 🔮 Future Improvements

The project can be extended with:

- Admin login system
- More adventure activities
- Trip availability management
- Booking history
- Email confirmation
- PDF invoice generation
- Web-based frontend
- React frontend
- Admin dashboard
- Online payment integration
- User authentication

---

## 👨‍💻 Developer

### Kunal Saxena

**BCA Graduate | MCA Student**

### Areas of Interest

- Python
- Web Development
- Backend Development
- Database Management
- AI/ML
- Software Development

---

## ⭐ Project Highlights

```text
Console-Based Application
        +
Python OOP
        +
MongoDB Atlas
        +
Input Validation
        +
Customer Management
        +
Adventure Trip Management
        +
Booking Management
        +
Payment Management
```

A practical Python project demonstrating how **Object-Oriented Programming and MongoDB** can be combined to build a real-world console application.

---

## 📄 License

This project is created for **educational and learning purposes**.
