from prettytable import PrettyTable
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.filedatabase
collection = db.savefile


def display_data():
    # Отримуємо всі документи з колекції
    documents = collection.find()
    # Створюємо таблицю
    table = PrettyTable()
    table.field_names = [
        "filename",
        "filehash",
        "upload_time",
        "upload_duration"
    ]
    for doc in documents:
        table.add_row(
            [
                doc['filename'],
                doc['filehash'],
                doc['upload_time'],
                doc['upload_duration']
            ]
        )
    print(table)


def get_filename_for_filehash(filehash):
    # повернення документу(словники, які зберігаються в nosql db)
    match = collection.find({'filehash': filehash})
    file_doc = match[0]
    return file_doc['filename']
