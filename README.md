# CITS3403-Project
Agile Web Development Project

Welcome to Love Letters, a heartfelt platform where you can share your stories, connect with others, and find love or friendship. To get started, simply create an account, browse through the posts, and don't forget to share your own love letter or friendship request!

| Name      | Student ID | Github Username |
| ----------- | ----------- | ----------- |
| Alex Hawking | 23354512 | Alex-Hawking |
| Akhil Gorasia | 23424609 | AkhilG4 |
| Martin Mitanoski | 23385544 | Mitan4E |
| Connor Grayden | 23349066 | Connor2803 |

Taskboard: [https://github.com/users/Alex-Hawking/projects/2](https://github.com/users/Alex-Hawking/projects/2)

# Set up
```
Clone the Repository:

  git clone https://github.com/Alex-Hawking/CITS3403-Project.git


Start and Initialise Virtual Environment:

  cd src

  python3 -m venv env

  source env/bin/activate

  pip install -r requirements.txt


Run the app:

  python3 app.py


Can connect via localhost:5000
```

# Testing
```
Start and Initialise Virtual Environment:

  cd src

  python3 -m venv env

  source env/bin/activate

  pip install -r requirements.txt


Run the testing:

  pytest src/tests/test_selenium.py
```


## Workflow

- New task in project (click on name of issue will open edit panel, make sure to add description)
- Assign yourself (click on name of issue will open edit panel, assign to you)
- Turn into issue
- Create branch from issue (MAKE SURE SOURCE IS DEVELOPMENT, should be change source option)
- Drag to in progress column
- Do code for issue (remember auto format on push so pull after)
- Pull request into development
- Pull request into main
- Close the issue with comments
- Drag into done column

## ACTIONS

**on push** to any branch, will automatically format code, so if you do a push (which you should only be doing for big changes), make sure to pull the formatted code a little bit after, this will ensure that the code we are storing on the repo is easy to read and looks good (also make sure you comment your code)

**on pull request** to any branch, will message the discord and will also request everyone to approve changes, ensure AT LEAST 2 approvals before merging (please review properly) 

# What we need to add

a description of the purpose of the application, explaining the its design and use.
a brief summary of the architecture of the application.
