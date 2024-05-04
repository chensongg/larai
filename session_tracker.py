import chromadb
import datetime

client = chromadb.Client()

collection = client.get_or_create_collection("visits")

def add_visit():
    collection.add(documents=[datetime.datetime.now()])

def get_visits():
