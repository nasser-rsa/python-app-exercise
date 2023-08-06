# Python App Exercise

This project aims to utilize the `ApiService` to fetch TODOs from an API and save them into the _storage_ folder.

## Table of Contents

- [Project Overview](#project-overview)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Tests](#tests)
- [GitHub Actions](#github-actions)
- [License](#license)

## Project Overview

- The goal is to fetch TODOs from a specific API URL: https://jsonplaceholder.typicode.com/todos/
- Each TODO should be saved in a separate file using the CSV format.
- The filename must contain the TODO "id" prefixed with the current date.
  - For example: 2021_04_28_123.csv

## Installation and Setup

1. Clone the repository to your local machine:

```bash
git clone https://github.com/nasser-rsa/python-app-exercise
```

2. Navigate to the project folder:

```bash
cd python-app-exercise
```

3. Create a virtual environment to isolate the project dependencies:

```bash
# On Windows
python -m venv .env

# On macOS and Linux
python3 -m venv .env
```

4. Activate the virtual environment:

```bash
# On Windows
.env\Scripts\activate

# On macOS and Linux
source .env/bin/activate
```

5. Upgrade pip to the latest version:

```bash
pip install --upgrade pip
```

6. Install the project dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To run the main program, execute the following command:

```bash
python main.py
```

## Tests

The project includes unit tests to ensure the correctness of the `ApiService` functionality. The test cases are located in the `tests` folder.

To run the tests, use the following command:

```bash
python -m unittest tests.test_apiservice
```

## GitHub Actions

The project includes a GitHub Actions workflow to automatically run tests whenever code is pushed to the `main` branch. The workflow configuration is defined in the `.github/workflows/test.yml` file.

The workflow sets up a matrix strategy to run tests with multiple Python versions (3.7, 3.8, 3.9, 3.10, and 3.11). It installs dependencies, runs unit tests using the `unittest` module, and executes the `main.py` script if the tests pass successfully.

## License

This project is licensed under the [MIT License](LICENSE). You can find a copy of the license in the LICENSE file.