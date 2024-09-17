This repository implements a simple task management logic similar to Jira. 
It is built using FASTapi and includes functionality for creating users with different roles for access. 
Authentication is handled through JWT tokens. Users can create, edit, and delete tasks, 
as well as retrieve a list of tasks and specific tasks by their ID. 
Additionally, there is a feature that simulates sending emails to task assignees when changes are made.

1. cloning the repository
    ```bash
   https://github.com/OlegBondarUA/task-tracker.git

2. Installation of a virtual environment
    ```bash
   python3 -m venv venv
   
3. Activate the virtual environment:
    ```bash
    # On Windows
    venv\Scripts\activate
-
    ```bash
    # On macOS or Linux
    source venv/bin/activate
  
4. Establishing dependencies
    ```bash
    pip install -r requirements.txt

5. Launch of the FASTapi project
    ```bash
   uvicorn main:app --reload
   
6. follow the link
    ```bash
   http://127.0.0.1:8000/docs
   
7. work verification and testing

In this section, you will set up users, who can either be assigned the role of a regular user or 
an admin (user/admin). Once a user is created, you’ll have the ability to create tasks, 
as well as edit or delete them as needed.