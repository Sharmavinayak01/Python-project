import re
from abc import ABC, abstractmethod

from database import Database


# =========================================================
# VALIDATION FUNCTIONS
# =========================================================

def validate_name(name):
    name = name.strip()

    if not name:
        return False

    return all(ch.isalpha() or ch.isspace() for ch in name)


def validate_mobile(mobile):
    return mobile.isdigit() and len(mobile) == 10


def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email.strip()) is not None


def get_positive_integer(message):
    while True:
        try:
            value = int(input(message).strip())

            if value > 0:
                return value

            print("Please enter a number greater than 0.")

        except ValueError:
            print("Please enter a valid number.")


def get_menu_choice(message, minimum, maximum):
    while True:
        try:
            value = int(input(message).strip())

            if minimum <= value <= maximum:
                return value

            print(f"Please select a number between {minimum} and {maximum}.")

        except ValueError:
            print("Please enter a valid number.")


# =========================================================
# BASE CLASS - ADVENTURE TRIP
# =========================================================

class AdventureTrip(ABC):

    def __init__(self, trip_id, name, location, duration, price):
        self.trip_id = trip_id
        self.name = name
        self.location = location
        self.duration = duration
        self.price = price

    @abstractmethod
    def calculate_cost(self, persons):
        pass

    def show_details(self):
        print("----------------------------------------")
        print("Trip ID   :", self.trip_id)
        print("Trip Name :", self.name)
        print("Location  :", self.location)
        print("Duration  :", self.duration, "Days")
        print("Price     : Rs.", self.price)
        print("----------------------------------------")


# =========================================================
# TREKKING TRIP
# =========================================================

class TrekkingTrip(AdventureTrip):

    def calculate_cost(self, persons):
        guide_charge = 1000
        return (self.price * persons) + guide_charge

    def show_details(self):
        print("\n========== TREKKING TRIP ==========")
        super().show_details()


# =========================================================
# RAFTING TRIP
# =========================================================

class RaftingTrip(AdventureTrip):

    def calculate_cost(self, persons):
        equipment_charge = 500 * persons
        return (self.price * persons) + equipment_charge

    def show_details(self):
        print("\n========== RAFTING TRIP ==========")
        super().show_details()


# =========================================================
# CAMPING TRIP
# =========================================================

class CampingTrip(AdventureTrip):

    def calculate_cost(self, persons):
        camping_charge = 700 * persons
        return (self.price * persons) + camping_charge

    def show_details(self):
        print("\n========== CAMPING TRIP ==========")
        super().show_details()


# =========================================================
# CUSTOMER CLASS
# =========================================================

class Customer:

    def __init__(self, customer_id, name, mobile, email):
        self.customer_id = customer_id
        self.name = name
        self.mobile = mobile
        self.email = email
        self.bookings = []

    def show_details(self):
        print("\n----------------------------------------")
        print("MongoDB ID :", self.customer_id)
        print("Name        :", self.name)
        print("Mobile      :", self.mobile)
        print("Email       :", self.email)
        print("----------------------------------------")


# =========================================================
# GUIDE CLASS
# =========================================================

class Guide:

    def __init__(self, guide_id, name, specialization):
        self.guide_id = guide_id
        self.name = name
        self.specialization = specialization

    def show_details(self):
        print("\nGuide ID       :", self.guide_id)
        print("Guide Name     :", self.name)
        print("Specialization :", self.specialization)


# =========================================================
# BOOKING CLASS
# =========================================================

class Booking:

    booking_counter = 1001

    def __init__(self, customer, trip, persons, guide):
        self.booking_id = Booking.booking_counter
        Booking.booking_counter += 1

        self.customer = customer
        self.trip = trip
        self.persons = persons
        self.guide = guide
        self.total_cost = trip.calculate_cost(persons)
        self.status = "Confirmed"
        self.payment_id = ""

    def show_booking(self):
        print("\n========================================")
        print("             BOOKING DETAILS")
        print("========================================")
        print("Booking ID   :", self.booking_id)
        print("Customer     :", self.customer.name)
        print("MongoDB ID   :", self.customer.customer_id)
        print("Trip         :", self.trip.name)
        print("Location     :", self.trip.location)
        print("Persons      :", self.persons)
        print("Duration     :", self.trip.duration, "Days")
        print("Guide        :", self.guide.name)
        print("Total Cost   : Rs.", self.total_cost)
        print("Payment ID   :", self.payment_id if self.payment_id else "Cash")
        print("Status       :", self.status)


# =========================================================
# PAYMENT CLASS - CONSOLE ONLY
# =========================================================

class Payment:

    def make_payment(self, amount):
        print("\n========================================")
        print("               PAYMENT")
        print("========================================")
        print("Amount to Pay : Rs.", amount)

        while True:
            print("\n1. UPI")
            print("2. Card")
            print("3. Cash")
            print("4. Cancel Payment")

            choice = input("\nSelect Payment Method: ").strip()

            # ---------------- UPI ----------------
            if choice == "1":
                print("\n----------------------------------------")
                print("             UPI PAYMENT")
                print("----------------------------------------")
                print("TEST MODE: No real money will be deducted.")

                upi_id = input("Enter UPI ID: ").strip()

                if not self.validate_upi(upi_id):
                    print("\nInvalid UPI ID!")
                    print("Example: kunal@upi")
                    continue

                print("\nProcessing UPI payment...")
                print("Payment Successful!")

                return {
                    "success": True,
                    "payment_id": "UPI-TEST",
                    "method": "UPI"
                }

            # ---------------- CARD ----------------
            elif choice == "2":
                print("\n----------------------------------------")
                print("             CARD PAYMENT")
                print("----------------------------------------")
                print("TEST MODE: No real money will be deducted.")

                card_number = input("Enter 16-digit Card Number: ").strip()

                if not card_number.isdigit() or len(card_number) != 16:
                    print("Invalid card number!")
                    continue

                cvv = input("Enter 3-digit CVV: ").strip()

                if not cvv.isdigit() or len(cvv) != 3:
                    print("Invalid CVV!")
                    continue

                print("\nProcessing card payment...")
                print("Payment Successful!")

                return {
                    "success": True,
                    "payment_id": "CARD-TEST",
                    "method": "Card"
                }

            # ---------------- CASH ----------------
            elif choice == "3":
                print("\nCash payment selected.")
                print("Payment marked as successful!")

                return {
                    "success": True,
                    "payment_id": "CASH",
                    "method": "Cash"
                }

            # ---------------- CANCEL ----------------
            elif choice == "4":
                print("\nPayment cancelled.")

                return {
                    "success": False,
                    "payment_id": "",
                    "method": ""
                }

            else:
                print("\nInvalid payment method!")
                print("Please select 1, 2, 3 or 4.")

    @staticmethod
    def validate_upi(upi_id):
        pattern = r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+$"
        return re.match(pattern, upi_id) is not None


# =========================================================
# MAIN MANAGEMENT CLASS
# =========================================================

class AdventureManagement:

    def __init__(self):
        # MongoDB Atlas connection
        self.db = Database()

        self.trips = [
            TrekkingTrip(
                1,
                "Himalayan Trek",
                "Manali",
                5,
                8500
            ),
            RaftingTrip(
                2,
                "River Rafting",
                "Rishikesh",
                2,
                3500
            ),
            CampingTrip(
                3,
                "Jungle Camping",
                "Jim Corbett",
                3,
                5000
            )
        ]

        self.guides = [
            Guide(1, "Vikas", "Trekking"),
            Guide(2, "Rahul", "River Rafting"),
            Guide(3, "Amit", "Camping")
        ]

        self.payment = Payment()

    # =====================================================
    # REGISTER CUSTOMER
    # =====================================================

    def register_customer(self):
        print("\n========================================")
        print("        CUSTOMER REGISTRATION")
        print("========================================")

        # Name
        while True:
            name = input("Enter Customer Name: ").strip()

            if validate_name(name):
                break

            print("Invalid name. Only alphabets and spaces are allowed.")

        # Mobile
        while True:
            mobile = input("Enter Mobile Number: ").strip()

            if validate_mobile(mobile):
                if self.db.mobile_exists(mobile):
                    print("This mobile number is already registered.")
                    continue
                break

            print("Invalid mobile number. Enter exactly 10 digits.")

        # Email
        while True:
            email = input("Enter Email: ").strip().lower()

            if not validate_email(email):
                print("Invalid email address.")
                continue

            if self.db.email_exists(email):
                print("This email is already registered.")
                continue

            break

        # Save in MongoDB
        customer_id = self.db.add_customer(
            name,
            mobile,
            email
        )

        if customer_id is None:
            print("\nCustomer could not be registered.")
            print("Mobile or email may already exist.")
            return None

        customer = Customer(
            customer_id,
            name,
            mobile,
            email
        )

        print("\n========================================")
        print("   CUSTOMER REGISTERED SUCCESSFULLY")
        print("========================================")
        print("Customer ID : 1")
        print("MongoDB ID  :", customer_id)
        print("Name        :", name)
        print("Mobile      :", mobile)
        print("Email       :", email)

        return customer

    # =====================================================
    # SHOW AVAILABLE TRIPS
    # =====================================================

    def show_trips(self):
        print("\n========================================")
        print("          AVAILABLE TRIPS")
        print("========================================")

        for trip in self.trips:
            trip.show_details()

    # =====================================================
    # SELECT EXISTING CUSTOMER
    # =====================================================

    def select_customer(self):
        customers = self.db.get_customers()

        if not customers:
            print("\nNo customers found.")
            print("Please register a customer first.")
            return None

        print("\n========================================")
        print("          SELECT CUSTOMER")
        print("========================================")

        for index, customer in enumerate(customers, 1):
            print(
                f"{index}. {customer['name']} - "
                f"{customer['mobile']}"
            )

        print("\n0. Cancel")

        while True:
            choice = input("\nSelect Customer: ").strip()

            try:
                choice = int(choice)

                if choice == 0:
                    return None

                if 1 <= choice <= len(customers):
                    data = customers[choice - 1]

                    return Customer(
                        data["id"],
                        data["name"],
                        data["mobile"],
                        data["email"]
                    )

                print("Invalid customer selection.")

            except ValueError:
                print("Please enter a valid number.")

    # =====================================================
    # SELECT TRIP
    # =====================================================

    def select_trip(self):
        print("\n========================================")
        print("             SELECT TRIP")
        print("========================================")

        for trip in self.trips:
            print(
                f"{trip.trip_id}. "
                f"{trip.name} - "
                f"{trip.location} - "
                f"Rs. {trip.price}"
            )

        print("0. Cancel")

        while True:
            choice = input("\nSelect Trip: ").strip()

            try:
                choice = int(choice)

                if choice == 0:
                    return None

                for trip in self.trips:
                    if trip.trip_id == choice:
                        return trip

                print("Invalid trip selection.")

            except ValueError:
                print("Please enter a valid number.")

    # =====================================================
    # SELECT GUIDE
    # =====================================================

    def select_guide(self, trip):
        print("\n========================================")
        print("             SELECT GUIDE")
        print("========================================")

        matching_guides = [
            guide
            for guide in self.guides
            if guide.specialization.lower()
            == self.get_specialization(trip).lower()
        ]

        # If no matching guide exists, show all guides
        if not matching_guides:
            matching_guides = self.guides

        for index, guide in enumerate(matching_guides, 1):
            print(
                f"{index}. {guide.name} "
                f"({guide.specialization})"
            )

        print("0. Cancel")

        while True:
            choice = input("\nSelect Guide: ").strip()

            try:
                choice = int(choice)

                if choice == 0:
                    return None

                if 1 <= choice <= len(matching_guides):
                    return matching_guides[choice - 1]

                print("Invalid guide selection.")

            except ValueError:
                print("Please enter a valid number.")

    @staticmethod
    def get_specialization(trip):
        if isinstance(trip, TrekkingTrip):
            return "Trekking"

        if isinstance(trip, RaftingTrip):
            return "River Rafting"

        if isinstance(trip, CampingTrip):
            return "Camping"

        return ""

    # =====================================================
    # CREATE BOOKING
    # =====================================================

    def create_booking(self):
        print("\n========================================")
        print("             CREATE BOOKING")
        print("========================================")

        # IMPORTANT:
        # Customer is NOT registered again.
        # We select an existing customer from MongoDB.
        customer = self.select_customer()

        if customer is None:
            return

        trip = self.select_trip()

        if trip is None:
            return

        guide = self.select_guide(trip)

        if guide is None:
            return

        persons = get_positive_integer(
            "\nEnter Number of Persons: "
        )

        # Calculate total cost using polymorphism
        total_cost = trip.calculate_cost(persons)

        print("\n========================================")
        print("             COST DETAILS")
        print("========================================")
        print("Trip Price        : Rs.", trip.price)
        print("Number of Persons :", persons)
        print("Guide             :", guide.name)
        print("Total Cost        : Rs.", total_cost)

        confirm = input(
            "\nConfirm Booking? (yes/no): "
        ).strip().lower()

        if confirm != "yes":
            print("\nBooking cancelled.")
            return

        # Payment
        payment_result = self.payment.make_payment(
            total_cost
        )

        if not payment_result["success"]:
            print("\nPayment failed/cancelled.")
            print(
                "Reason :",
                "Payment cancelled or invalid details."
            )
            print("Booking was NOT created.")
            return

        # Create booking object
        booking = Booking(
            customer,
            trip,
            persons,
            guide
        )

        booking.payment_id = payment_result["payment_id"]

        # Save booking in MongoDB
        booking_id = self.db.add_booking(
            customer_id=customer.customer_id,
            trip_id=trip.trip_id,
            trip_name=trip.name,
            persons=persons,
            guide_name=guide.name,
            total_cost=total_cost,
            payment_id=payment_result["payment_id"]
        )

        booking.show_booking()

        print("\n========================================")
        print("       BOOKING CREATED SUCCESSFULLY")
        print("========================================")
        print("MongoDB Booking ID :", booking_id)

    # =====================================================
    # VIEW ALL CUSTOMERS
    # =====================================================

    def view_all_customers(self):
        customers = self.db.get_customers()

        print("\n========================================")
        print("            ALL CUSTOMERS")
        print("========================================")

        if not customers:
            print("No customers found.")
            return

        for customer_data in customers:
            customer = Customer(
                customer_data["id"],
                customer_data["name"],
                customer_data["mobile"],
                customer_data["email"]
            )

            customer.show_details()

    # =====================================================
    # VIEW CUSTOMER BOOKINGS
    # =====================================================

    def view_customer_bookings(self):
        customer = self.select_customer()

        if customer is None:
            return

        bookings = self.db.get_bookings(
            customer.customer_id
        )

        print("\n========================================")
        print("        CUSTOMER BOOKINGS")
        print("========================================")

        if not bookings:
            print("No bookings found for this customer.")
            return

        for booking in bookings:
            print("\n----------------------------------------")
            print("Booking MongoDB ID :", booking["id"])
            print("Customer           :", customer.name)
            print("Trip               :", booking["trip_name"])
            print("Trip ID            :", booking["trip_id"])
            print("Persons            :", booking["persons"])
            print("Guide              :", booking["guide_name"])
            print("Total Cost         : Rs.", booking["total_cost"])
            print("Payment ID         :", booking["payment_id"])
            print("Status             :", booking["status"])
            print("----------------------------------------")

    # =====================================================
    # CANCEL BOOKING
    # =====================================================

    def cancel_booking(self):
        customer = self.select_customer()

        if customer is None:
            return

        bookings = self.db.get_bookings(
            customer.customer_id
        )

        if not bookings:
            print("\nNo bookings found for this customer.")
            return

        print("\n========================================")
        print("          YOUR BOOKINGS")
        print("========================================")

        for index, booking in enumerate(bookings, 1):
            print(
                f"{index}. {booking['trip_name']} | "
                f"Rs. {booking['total_cost']} | "
                f"Status: {booking['status']}"
            )

        print("0. Cancel")

        choice = get_menu_choice(
            "\nSelect Booking: ",
            0,
            len(bookings)
        )

        if choice == 0:
            return

        selected_booking = bookings[choice - 1]

        if selected_booking["status"] == "Cancelled":
            print("\nThis booking is already cancelled.")
            return

        confirm = input(
            "Are you sure you want to cancel? (yes/no): "
        ).strip().lower()

        if confirm != "yes":
            print("\nCancellation aborted.")
            return

        success = self.db.cancel_booking(
            selected_booking["id"]
        )

        if success:
            print("\nBooking cancelled successfully.")
            print(
                "Booking MongoDB ID :",
                selected_booking["id"]
            )
        else:
            print("\nBooking cancellation failed.")

    # =====================================================
    # MAIN MENU
    # =====================================================

    def run(self):

        try:
            while True:

                print("\n========================================")
                print("       ADVENTURE TRIP MANAGEMENT")
                print("========================================")
                print("1. Register Customer")
                print("2. Show Available Trips")
                print("3. Create Booking")
                print("4. View All Customers")
                print("5. View Customer Bookings")
                print("6. Cancel Booking")
                print("7. Exit")

                choice = input(
                    "\nEnter your choice: "
                ).strip()

                if choice == "1":
                    self.register_customer()

                elif choice == "2":
                    self.show_trips()

                elif choice == "3":
                    self.create_booking()

                elif choice == "4":
                    self.view_all_customers()

                elif choice == "5":
                    self.view_customer_bookings()

                elif choice == "6":
                    self.cancel_booking()

                elif choice == "7":
                    print("\nThank you for using Adventure Trip Management.")
                    break

                else:
                    print("\nInvalid choice!")
                    print("Please select 1 to 7.")

        except KeyboardInterrupt:
            print("\n\nProgram stopped by user.")

        finally:
            self.db.close()


# =========================================================
# PROGRAM START
# =========================================================

if __name__ == "__main__":
    app = AdventureManagement()
    app.run()
