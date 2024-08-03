#! /bin/env python3

""" Issues client operations """

import sys

from random import randint
from multiprocessing import Process

from pymongo import MongoClient

def _main():
    db_addr = sys.argv[1]
    num_entries = int(sys.argv[2])
    client_multiply = int(sys.argv[3])
    num_ops = int(sys.argv[4])
    write_chance = int(sys.argv[5])

    # Launch client processes
    processes = []
    for _ in range(client_multiply):
        args = (db_addr, write_chance, num_entries, num_ops)
        proc = Process(target=run_client, args=args)
        proc.start()
        processes.append(proc)

    for proc in processes:
        proc.join()

def run_client(db_addr, write_chance, num_entries, num_ops):
    """ Runs a client process that issues operations to MongoDB """

    client = MongoClient(db_addr)
    collection = client.test_database.test_collection

    for _ in range(num_ops):
        is_write = randint(0,100) < write_chance
        entry_id = str(randint(0, num_entries))

        if is_write:
            _ = collection.update_one({"_id": entry_id}, {'value', 'the new value'})
        else:
            _ = collection.find_one({"_id": entry_id})

if __name__ == "__main__":
    _main()
