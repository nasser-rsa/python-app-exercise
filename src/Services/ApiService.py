import os
from sys import stderr
from datetime import datetime
import csv
import requests


class ApiService:
    def __init__(self, storage_folder=os.path.join(os.getcwd(), 'storage')):
        self.url = 'https://jsonplaceholder.typicode.com/todos/'
        self.storage_folder = storage_folder

    def fetch_todos(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching from the API: {e}")
            return None

    def create_csv_file(self, todo):
        try:
            todo_id = todo['id']
            user_id = todo['userId']
            title = todo['title']
            completed = todo['completed']

            file_name = f"{datetime.now().strftime('%Y_%m_%d')}_{todo_id}.csv"
            file_path = os.path.join(self.storage_folder, file_name)

            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'userId', 'title', 'completed'])
                writer.writerow([todo_id, user_id, title, completed])
            return True
        except (KeyError, IOError) as e:
            print(f"Error processing todo: {e}")
            return False

    def run(self):
        print('Running ApiService')

        if not os.path.exists(self.storage_folder):
            os.makedirs(self.storage_folder)

        todos = self.fetch_todos()
        if todos:
            success = True  # Flag to track if any exception occurred
            for todo in todos:
                if not self.create_csv_file(todo):
                    success = False

            if success:
                print("TODOs fetched and saved as CSV files successfully")


if __name__ == "__main__":
    api_service = ApiService()
    api_service.run()
