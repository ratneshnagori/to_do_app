## Introduction :

This is a basic Web App to maintain a to-do list. 

Requirements:

* Python3 with Flask framework
* Moden browser
* Terminal

### Installation instruction:

1. Download and install python3 - [Download](https://www.python.org/downloads/)
   
   ```
   $sudo apt install python3
   ```
   
2. Install pip3 for python 3 -
   
   ```
   $sudo apt install python3-pip
   ```
   
2. Download and install Flask framework - [Download](https://flask.palletsprojects.com/en/1.1.x/installation/)
   
   ```
   $pip3 install Flask
   ```

3. Download to_do_app.zip from Git or email.

4. Unzip content of to_do_app.zip

5. Go to unzipped directory where all folders, .py and .db files are stored.

6. Go to terminal and execute command - 
   
   ```
   $python3 to_do_app.py
   ```

## Usage:

Go to browser and enter below URL in address bar-

http://127.0.0.1:5000/

## Web interface

Web interface is self explantory with function such as:

* **Add a new to-do task**
* **Edit/Delete/Mark complete the task**
* **Filter tasks**

## Few utilities

* **Current date at top for reference**
* **Total number of tasks at bottom**

## Interact with API using CLI

1. Add a task -
	
   ```	  
   curl -X POST http://127.0.0.1:5000/api/v1/add_task -d '{"task": "Task1", "details": "Contact John Doe about project X", "duedate": "2020-10-31"}' -H 'Content-Type: application/json'
   ```
   Initially when a new task is added, its **status** by default is **Pending**. 
2. Complete a task -
   
   ```
   curl -X PUT http://127.0.0.1:5000/api/v1/complete_task -d '{"task": "Task1", "status":"Completed"}' -H 'Content-Type: application/json'
   ```
    
3. Update a task-
   
   ```
   curl -X PUT http://127.0.0.1:5000/api/v1/edit_task -d '{"task": "Task1", "details": "Contact John Doe about project X and arrange meeting too.", "duedate": "2020-10-31", "status":"Completed"}' -H 'Content-Type: application/json'
   ```
   
4. Delete task -
   
   ```   
   curl -X DELETE http://127.0.0.1:5000/api/v1/delete_task -d '{"task": "Task1"}' -H 'Content-Type: application/json'
   ```
            
5. Get all task - 
   
   ```
   curl -X GET http://127.0.0.1:5000/api/v1/all_tasks
   ```
