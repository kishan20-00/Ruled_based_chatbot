from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb+srv://Kishan:luka2000@cluster0.2g59arm.mongodb.net/")
db = client["chatbot_db"]
marks_collection = db["marks"]

# Sample data
sample_data = [
    {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "semester": 1,
        "marks": {
            "subject1": 85,
            "subject2": 90,
            "subject3": 78
        }
    },
    {
        "name": "Jane Smith",
        "email": "janesmith@example.com",
        "semester": 2,
        "marks": {
            "subject1": 88,
            "subject2": 92,
            "subject3": 81
        }
    },
    {
        "name": "Mike Johnson",
        "email": "mikejohnson@example.com",
        "semester": 3,
        "marks": {
            "subject1": 75,
            "subject2": 80,
            "subject3": 85
        }
    },
    {
        "name": "Emily Clark",
        "email": "emilyclark@example.com",
        "semester": 4,
        "marks": {
            "subject1": 89,
            "subject2": 95,
            "subject3": 92
        }
    }
]

# Inserting sample data into the marks collection
marks_collection.insert_many(sample_data)

print("Sample data inserted successfully!")
