# CITS3403-Project
Agile Web Development Project

Welcome to Love Letters, a heartfelt platform where you can share your stories, connect with others, and find love or friendship. To get started, simply create an account, browse through the posts, and don't forget to share your own love letter or friendship request!


# Set up
```
Clone the Repository


Start and Initialise Virtual Environment:

  python3 -m venv env

  source src/env/bin/activate

  pip install -r src/requirements.txt

Initialize test database:

  python3 generate_example_db.py

```

# Running

```
Set up steps are completed as above (db is created and are in venv).

From main directory:

  python3 ./src/app.py

Can now access site on localhost:5000
```

# Testing
```
Start and Initialise Virtual Environment:

  cd src

  python3 -m venv env

  source env/bin/activate

  pip install -r requirements.txt


Reset database and run the testing:

  python3 generate_example_db.py

  pytest src/tests/test_selenium.py
```

