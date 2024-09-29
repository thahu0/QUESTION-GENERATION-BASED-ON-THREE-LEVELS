from flask_pymongo import PyMongo

def check_mongo_connection(app):
    try:
        mongo = PyMongo(app)
        # Access a specific database (replace 'your_database_name' with your actual database name)
        db = mongo.db.mini
        names = db.list_collection_names()
        print("Connected Successfully", names)
    except Exception as e:
        print(f"Failed to connect to MongoDB: {str(e)}")
