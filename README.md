# CITS3403-Project
Agile Web Dev Project

# Set up
```
git clone https://github.com/Alex-Hawking/CITS3403-Project.git

start virtual env (all within src):

python3 -m venv env

source env/bin/activate

(when done: deactivate)

pip install -r requirements.txt (from src/)

python3 app.py
```

Will be on localhost (idk which port)

## Workflow

- New task in project
- Assign yourself
- Turn into issue
- Create branch from issue (MAKE SURE SOURCE IS DEVELOPMENT)
- Do code for issue (remember auto format on push)
- Pull request into development (2 approved reviews)
- Pull request into main (2 approved reviews)

## ACTIONS

**on push** to any branch, will automatically format code, so if you do a push (which you should only be doing for big changes), make sure to pull the formatted code a little bit after, this will ensure that the code we are storing on the repo is easy to read and looks good (also make sure you comment your code)

**on pull request** to any branch, will message the discord and will also request everyone to approve changes, ensure AT LEAST 2 approvals before merging (please review properly) 

# What we need to add

a description of the purpose of the application, explaining the its design and use.

a table with with each row containing the i) UWA ID ii) name and iii) Github user name of the group members.

a brief summary of the architecture of the application.

instructions for how to launch the application.

instructions for how to run the tests for the application.
