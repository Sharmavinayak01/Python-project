from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()


class Database:
    def __init__(self):
        uri = os.getenv("MONGODB_URI")

        if not uri:
            raise RuntimeError(
                "MONGODB_URI missing in .env file."
            )

        try:
            self.client = MongoClient(
                uri,
                serverSelectionTimeoutMS=10000
            )
            self.client.admin.command("ping")
            print("MongoDB Atlas connected successfully!")

        except Exception as error:
            print("MongoDB connection failed!")
            print("Reason:", error)
            raise

        self.db = self.client["adventure_trip"]
        self.customers = self.db["customers"]
        self.bookings = self.db["bookings"]

        self.customers.create_index("mobile", unique=True)
        self.customers.create_index("email", unique=True)

    def add_customer(self, name, mobile, email):
        try:
            result = self.customers.insert_one({
                "name": name,
                "mobile": mobile,
                "email": email
            })
            return str(result.inserted_id)
        except DuplicateKeyError:
            return None

    def get_customer(self, customer_id):
        try:
            doc = self.customers.find_one({
                "_id": ObjectId(customer_id)
            })
            if doc:
                doc["id"] = str(doc["_id"])
                return doc
        except Exception:
            pass
        return None

    def get_customers(self):
        result = []
        for doc in self.customers.find().sort("_id", 1):
            doc["id"] = str(doc["_id"])
            result.append(doc)
        return result

    def mobile_exists(self, mobile):
        return self.customers.find_one({"mobile": mobile}) is not None

    def email_exists(self, email):
        return self.customers.find_one({"email": email}) is not None

    def add_booking(
        self,
        customer_id,
        trip_id,
        trip_name,
        persons,
        guide_name,
        total_cost,
        payment_id
    ):
        result = self.bookings.insert_one({
            "customer_id": customer_id,
            "trip_id": trip_id,
            "trip_name": trip_name,
            "persons": persons,
            "guide_name": guide_name,
            "total_cost": total_cost,
            "payment_id": payment_id,
            "status": "Confirmed"
        })
        return str(result.inserted_id)

    def get_booking(self, booking_id):
        try:
            doc = self.bookings.find_one({
                "_id": ObjectId(booking_id)
            })
            if doc:
                doc["id"] = str(doc["_id"])
                return doc
        except Exception:
            pass
        return None

    def get_bookings(self, customer_id):
        result = []
        for doc in self.bookings.find({
            "customer_id": customer_id
        }).sort("_id", -1):
            doc["id"] = str(doc["_id"])
            result.append(doc)
        return result

    def cancel_booking(self, booking_id):
        try:
            result = self.bookings.update_one(
                {"_id": ObjectId(booking_id)},
                {"$set": {"status": "Cancelled"}}
            )
            return result.matched_count == 1
        except Exception:
            return False

    def close(self):
        self.client.close()
        print("MongoDB connection closed.")
