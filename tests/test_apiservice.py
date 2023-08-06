import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import os
import csv
import src.Services.ApiService
import requests


class TestApiService(unittest.TestCase):
    def setUp(self):
        # Clean up CSV files in the storage folder before each test
        storage_folder = os.path.join(os.getcwd(), 'storage')
        if os.path.exists(storage_folder):
            for file in os.listdir(storage_folder):
                if file.endswith(".csv"):
                    file_path = os.path.join(storage_folder, file)
                    os.remove(file_path)

        self.good_todos = [
            {"id": 1, "userId": 1, "title": "Todo 1", "completed": False},
            {"id": 2, "userId": 1, "title": "Todo 2", "completed": True},
        ]

        self.wrong_todos = [
            {"ID": 1, "UserID": 1, "Task": "Todo 1", "IsCompleted": False},
            {"ID": 2, "UserID": 1, "Task": "Todo 2", "IsCompleted": True},
        ]

    @patch('src.Services.ApiService.requests.get')
    def test_run(self, mock_get):
        # Mock the response object
        mock_response = MagicMock()
        mock_response.status_code = 200  # Successful response
        mock_response.json.return_value = self.good_todos
        mock_get.return_value = mock_response

        # Call the ApiService.run() method
        api_service = src.Services.ApiService.ApiService()
        api_service.run()

        # Assert that the CSV files are created successfully
        storage_folder = os.path.join(os.getcwd(), 'storage')
        self.assertTrue(os.path.exists(storage_folder))

        for todo in self.good_todos:
            file_name = f"{datetime.now().strftime('%Y_%m_%d')}_{todo['id']}.csv"
            file_path = os.path.join(storage_folder, file_name)
            self.assertTrue(os.path.exists(file_path))

            # Read the CSV file and check if data matches
            with open(file_path, mode='r') as file:
                reader = csv.reader(file)
                header = next(reader)
                self.assertEqual(
                    header, ['id', 'userId', 'title', 'completed'])

                data = next(reader)
                self.assertEqual(int(data[0]), todo['id'])
                self.assertEqual(int(data[1]), todo['userId'])
                self.assertEqual(data[2], todo['title'])
                self.assertEqual(data[3], str(todo['completed']))

    @patch('src.Services.ApiService.requests.get')
    def test_run_wrong_keys(self, mock_get):
        # Mock the response object for good calls with wrong keys
        mock_response = MagicMock()
        mock_response.status_code = 200  # Successful response
        mock_response.json.return_value = self.wrong_todos
        mock_response.raise_for_status.side_effect = None
        mock_get.return_value = mock_response

        # Call the ApiService.run() method
        api_service = src.Services.ApiService.ApiService()
        api_service.run()

        # Assert that the storage folder is created
        storage_folder = os.path.join(os.getcwd(), 'storage')
        self.assertTrue(os.path.exists(storage_folder))

        # Assert that no CSV files are created due to the wrong keys in the response
        for todo in self.wrong_todos:
            file_name = f"{datetime.now().strftime('%Y_%m_%d')}_{todo['ID']}.csv"
            file_path = os.path.join(storage_folder, file_name)
            self.assertFalse(os.path.exists(file_path))

    @patch('src.Services.ApiService.requests.get')
    def test_run_empty_keys(self, mock_get):
        # Mock the response object for wrong calls with missing keys
        mock_response = MagicMock()
        mock_response.status_code = 200  # Successful response
        mock_response.json.return_value = [{}]  # Simulate missing keys
        mock_response.raise_for_status.side_effect = None
        mock_get.return_value = mock_response

        # Call the ApiService.run() method
        api_service = src.Services.ApiService.ApiService()
        api_service.run()

        # Assert that the storage folder is created
        storage_folder = os.path.join(os.getcwd(), 'storage')
        self.assertTrue(os.path.exists(storage_folder))

        # Assert that no CSV files are created due to missing keys in the response
        # Invalid file name due to missing ID
        file_name = f"{datetime.now().strftime('%Y_%m_%d')}_.csv"
        file_path = os.path.join(storage_folder, file_name)
        self.assertFalse(os.path.exists(file_path))

    @patch('src.Services.ApiService.requests.get')
    def test_run_api_not_found_error(self, mock_get):
        # Mock the response object with a 404 status code
        mock_response = MagicMock()
        mock_response.status_code = 404  # Not Found
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "404 Client Error: Not Found")
        mock_get.return_value = mock_response

        # Call the ApiService.run() method
        api_service = src.Services.ApiService.ApiService()
        api_service.run()

        # Assert that the storage folder is created
        storage_folder = os.path.join(os.getcwd(), 'storage')
        self.assertTrue(os.path.exists(storage_folder))

        # Assert that no CSV files are created due to the error response
        for todo in self.good_todos:
            file_name = f"{datetime.now().strftime('%Y_%m_%d')}_{todo['id']}.csv"
            file_path = os.path.join(storage_folder, file_name)
            self.assertFalse(os.path.exists(file_path))

    @patch('src.Services.ApiService.requests.get')
    def test_run_server_error(self, mock_get):
        # Mock the response object with a 500 status code
        mock_response = MagicMock()
        mock_response.status_code = 500  # Internal Server Error
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "500 Server Error")
        mock_get.return_value = mock_response

        # Call the ApiService.run() method
        api_service = src.Services.ApiService.ApiService()
        api_service.run()

        # Assert that the storage folder is created
        storage_folder = os.path.join(os.getcwd(), 'storage')
        self.assertTrue(os.path.exists(storage_folder))

        # Assert that no CSV files are created due to the error response
        for todo in self.good_todos:
            file_name = f"{datetime.now().strftime('%Y_%m_%d')}_{todo['id']}.csv"
            file_path = os.path.join(storage_folder, file_name)
            self.assertFalse(os.path.exists(file_path))


if __name__ == '__main__':
    unittest.main()
