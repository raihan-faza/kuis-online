from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# uri = "mongodb+srv://asyrafna:nugiGOJ2Gcu8nf59@quiz.skssdkk.mongodb.net/?retryWrites=true&w=majority&appName=Quiz"
uri = "mongodb+srv://syaidtengku:jj7g0yeWtciAuOV9@cluster0.rmjjkij.mongodb.net/ccloud"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.Quiz

grade_collection = db['grade_list']
simulate_collection = db['simulation_list']
real_grade = db['real_list']

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)