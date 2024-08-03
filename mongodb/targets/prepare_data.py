#! /bin/env python3

""" Sets up the data for our benchmark """

import sys

from pymongo import MongoClient

db_addr = sys.argv[1]
num_entries = int(sys.argv[2])

client = MongoClient(db_addr)
db = client.test_database
collection = db.test_collection

for idx in range(num_entries):
    collection.insert_one({
        "_id": str(idx),
        "value": "here is some data",
    })
