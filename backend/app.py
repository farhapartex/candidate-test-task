import os
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from main import CSVParser

PROJECT_PATH = os.path.abspath(".")

app = Flask(__name__)

CORS(app, support_credentials=True)

@app.route("/")
def get_transactions():
    try:
        files = os.listdir(f'{PROJECT_PATH}/exchange_files')
    except FileNotFoundError as error:
        return jsonify({"error": "Sorry! File not found"}), 500

    transactions = []

    try:
        for file in files:
            file_split_list = file.split(".")
            if file_split_list[-1] == "csv":
                parser = CSVParser(f'exchange_files/{file}')
                transactions += parser.get_json_results()
    except Exception as error:
        return jsonify({"error": str(error)})

    return jsonify({"transactions": transactions})

