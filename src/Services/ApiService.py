import os
from sys import stderr
from datetime import datetime
import csv
import requests

URL = 'https://jsonplaceholder.typicode.com/todos/'
STORAGE_FOLDER = os.path.join(os.getcwd(), 'storage')


def fetch_todos():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from the API: {e}", file=stderr)
        return None


class ApiService:
    def __init__(self):
        pass

    def run(self):
        print('Running ApiService')

        if not os.path.exists(STORAGE_FOLDER):
            os.makedirs(STORAGE_FOLDER)

        todos = fetch_todos()
        if todos:
            success = True  # Flag to track if any exception occurred
            for todo in todos:
                try:
                    # Check for the required keys and handle errors gracefully
                    todo_id = todo['id']
                    user_id = todo['userId']
                    title = todo['title']
                    completed = todo['completed']

                    file_name = f"{datetime.now().strftime('%Y_%m_%d')}_{todo_id}.csv"
                    file_path = os.path.join(STORAGE_FOLDER, file_name)

                    try:
                        with open(file_path, mode='w', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(
                                ['id', 'userId', 'title', 'completed'])
                            writer.writerow(
                                [todo_id, user_id, title, completed])
                    except IOError as e:
                        print(
                            f"Error writing to file {file_name}: {e}", file=stderr)
                        success = False

                except KeyError as e:
                    print(f"Error processing todo: {e}", file=stderr)
                    success = False

            if success:
                print("TODOs fetched and saved as CSV files successfully")
