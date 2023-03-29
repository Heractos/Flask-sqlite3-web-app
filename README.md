# Flask-sqlite3-web-app

## Setup & Installation

Make sure you have the latest version of Python installed.

To begin hosting our web application, the first step is to access the virtual environment. This environment has been specifically set up with pre-installed modules based on our app's dependencies and requirements.

```bash
source env/bin/activate
```

To ensure that all dependencies are correctly installed, you can execute the following command to reinstall all modules:

```bash
pip install -r requirements.txt
```

This will verify that all necessary packages are present and up-to-date.

## Running The App

To properly execute the application, please execute the command below in your terminal:

```bash
python main.py
```

## Viewing The App

To access our application, kindly follow the link provided below where it is hosted: `http://127.0.0.1:5000`

## Preloaded Database Content

Our application is integrated with a pre-existing database. As part of the testing process, I have created two user accounts within the database. Each account has authored two posts, engaged in reciprocal post liking, and commented on each other's posts.

## If 403 Error Encountered

Just in case, if you encounter 403 error from your browser (applies to Chrome only), you can use this link to flush socket pools:
`chrome://net-internals/#sockets`
