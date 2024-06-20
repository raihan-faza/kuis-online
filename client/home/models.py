from django.db import models

# Create your models here.
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# uri = "mongodb+srv://asyrafna:nugiGOJ2Gcu8nf59@quiz.skssdkk.mongodb.net/?retryWrites=true&w=majority&appName=Quiz"
uri = "mongodb+srv://syaidtengku:jj7g0yeWtciAuOV9@cluster0.rmjjkij.mongodb.net/ccloud"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['Quiz'] 
quiz_collection = db['grade_list']  # Replace with your collection name

class Product(models.Model):
    id    = models.AutoField(primary_key=True)
    name  = models.CharField(max_length = 100) 
    info  = models.CharField(max_length = 100, default = '')
    price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
   