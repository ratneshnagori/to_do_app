import db_functions
import json
from flask import Flask, render_template, flash, request, Response
from datetime import datetime
import datetime

app = Flask(__name__)

SUCCESS='Success'
FAILURE = 'Failure'
sort_status = 0
    
#Display webpage with all to-do tasks
@app.route('/app')
def home_page():

    data = db_functions.get_all_tasks()
        
    updated_data =[]
    for task in data:
        updated_data.append(get_tasks_with_days_left(task))
    return render_template('to_do.html', data = updated_data)

#Trigger sorting by due date and display table
@app.route('/toggleSorting')
def home_page_sorted():
    global sort_status
    if sort_status == 0:
        data = db_functions.get_all_tasks_sorted(sort_status)
        sort_status = 1
    else:
        data = db_functions.get_all_tasks_sorted(sort_status)
        sort_status = 0
    updated_data =[]
    for task in data:
        updated_data.append(get_tasks_with_days_left(task))
    return render_template('to_do.html', data = updated_data)
    
#For API call from CLI
@app.route('/api/v1/all_tasks')
def get_all_items():
    # Get items from the db
    db_data = db_functions.get_all_tasks()

    # Return response
    response = Response(json.dumps(db_data), mimetype='application/json')
    return response
    
#Wrapper when API call is made from Webpage
@app.route('/add_task_from_html', methods=['POST'])
def add_task_from_html():
    # Get details from the HTML form
    req_data = request.form
    
    task = req_data.get("task")
    duedate = req_data.get("duedate")
    details = req_data.get("details")
    result = add_task(task, details, duedate)
    if "error" in result:
        return result
        
    data = db_functions.get_all_tasks()
    updated_data =[]
    for task in data:
        updated_data.append(get_tasks_with_days_left(task))
    return render_template('to_do.html', data = updated_data)

#Function for API call to add a new task to DB using CLI. add_task_from_html() utilize this when call is made from webpage     
@app.route('/api/v1/add_task', methods=['POST'])
def add_task(*args):
    try:
	    if len(args) == 0:
	        req_data = request.get_json()
	        task = req_data['task']
	        details = req_data['details']
	        duedate = req_data['duedate']
	    else:
	        task = args[0]
	        details = args[1]
	        duedate = args[2]
	    try:
	        datetime.datetime.strptime(duedate, '%Y-%m-%d')
	    except ValueError:
	        try:
	            duedate = datetime.datetime.strptime(duedate, '%d/%m/%Y').strftime('%Y-%m-%d')
	        except:
	            error = "error: incorrect date format, must be DD/MM/YYYY"
	            return error
	        
	    # Add item to the list
	    db_data = db_functions.add_a_task(task, details, duedate)

	    # Return error if item not added
	    if db_data['Result'] == 'Failure':
	        if "UNIQUE constraint failed" in db_data['Remark']:
	             db_data['Remark'] = "Task exists in the list"
	        response = "error: task could not be added, reason: " + db_data['Remark']
	        return response
	
	    # Return response
	    response = "success: task added to the list"
	    return response
	    
    except Exception as e:
	    error = {"Error": "There is some error with API call, please check its format"}
	    if not datetime.datetime.strptime(duedate, '%d/%m/%Y'):
	        error = {"Error": "Incorrect date format, must be DD/MM/YYYY"}
	    return error 

#Wrapper when API call is made from Webpage
@app.route('/edit_task_from_html', methods=['POST'])
def edit_task_from_html():
    # Get details from the HTML form
    req_data = request.form
    
    task = req_data.get("task")
    duedate = req_data.get("duedate")
    details = req_data.get("details")
    status = req_data.get("status")
    result = edit_task(task, details, duedate, status)
    if "error" in result:
        return result
        
    data = db_functions.get_all_tasks()
    updated_data =[]
    for task in data:
        updated_data.append(get_tasks_with_days_left(task))
    return render_template('to_do.html', data = updated_data)

#Function for API call to edit a task in DB using CLI. edit_task_from_html() utilize this when call is made from webpage        
@app.route('/api/v1/edit_task', methods=['PUT'])
def edit_task(*args):
    try:
	    if len(args) == 0:
	        req_data = request.get_json()
	        task = req_data['task']
	        details = req_data['details']
	        duedate = req_data['duedate']
	        status = req_data['status']
	    else:
	        task = args[0]
	        details = args[1]
	        duedate = args[2]
	        status = args[3]
	    try:
	        datetime.datetime.strptime(duedate, '%Y-%m-%d')
	    except ValueError:
	        try:
	            duedate = datetime.datetime.strptime(duedate, '%d/%m/%Y').strftime('%Y-%m-%d')
	        except:
	            error = "error: incorrect date format, must be DD/MM/YYYY"
	            return error
        
	    #edit item
	    db_data = db_functions.update_task(task, details, duedate, status)
	    # Return error if item not edited
	    if db_data['Result'] == 'Failure':
	        response = "error: task could not be edited, reason: " + db_data['Remark']
	        return response
	
	    # Return response
	    response = "success: task successfully edited"
	    return response
	    
    except Exception as e:
	    error = "Error There is some error with API call, please check its format"
	    return error 

#Wrapper when API call is made from Webpage
@app.route('/complete_task_from_html', methods=['POST'])
def complete_task_from_html():
    # Get task in JSON from frontend AJAX call

    task = request.json['task']
    result = complete_task(task)
    
    if "error" in result:
        return result
        
    data = db_functions.get_all_tasks()
    updated_data =[]
    for task in data:
        updated_data.append(get_tasks_with_days_left(task))
    return render_template('to_do.html', data = updated_data)

#Function for API call to complete a task in DB using CLI. complete_task_from_html() utilize this when call is made from webpage        
@app.route('/api/v1/complete_task', methods=['PUT'])
def complete_task(*args):
    try:
        status = "Completed"
        if len(args) == 0:
            req_data = request.get_json()
            task = req_data['task']
        else:
	        task = args[0]
	    
	    #Mark task as completed
        db_data = db_functions.update_task_status(task, status)
        
        # Return error if status is not completed
        if db_data['Result'] == 'Failure':
	        response = "error: task could marked completed, reason: " + db_data['Remark']
	        return response
	
	    # Return response
        response = "success: task completed successfully"
        return response
	    
    except Exception as e:
	    error = {"Error": "There is some error with API call, please check its format"}
	    response = Response(json.dumps(error), mimetype='application/json')
	    return response 

#Wrapper when API call is made from Webpage
@app.route('/delete_task_from_html', methods=['POST'])
def delete_task_from_html():
    # Get details from the HTML form
    req_data = request.form
    
    task = req_data.get("task")
    
    result = delete_task(task)
    
    if "error" in result:
        return result
        
    data = db_functions.get_all_tasks()
    updated_data =[]
    for task in data:
        updated_data.append(get_tasks_with_days_left(task))
    return render_template('to_do.html', data = updated_data)

#Function for API call to delete a task from DB using CLI. delete_task_from_html() utilize this when call is made from webpage            
@app.route('/api/v1/delete_task', methods=['DELETE'])
def delete_task(*args):
    try:
	    if len(args) == 0:
	        req_data = request.get_json()
	        task = req_data['task']
	    else:
	        task = args[0]
	        
	    # Remove task from the list
	    db_data = db_functions.delete_item(task)

	    # Return error if item not deleted
	    if db_data['Result'] == 'Failure':
	        response = "error: task could not be deleted, reason: " + db_data['Remark']
	        return response
	
	    # Return response
	    response = "success: task deleted from list"
	    return response
	    
    except Exception as e:
	    error = {"Error": "There is some error with API call, please check its format"}
	    response = Response(json.dumps(error), mimetype='application/json')
	    return response 

#Function to calculate number of days left for task and add date in dd/mm/yyyy format in task tuple
def get_tasks_with_days_left(data):
    try:
        data_list = list(data)
        if data_list[3] == "Completed":
            data_list.append("-")
        else:
            current_date = datetime.date.today()
            task_duedate = datetime.datetime(int(data_list[2].split("-")[0]),int(data_list[2].split("-")[1]),int(data_list[2].split("-")[2])).date()
            data_list.append(str((task_duedate-current_date).days))
        data_list.append(data_list[2].split("-")[2]+"/"+data_list[2].split("-")[1]+"/"+data_list[2].split("-")[0])
        data = tuple(data_list)
        
        return data
    except Exception as e:
	    error = {"Error": "Issue while updating date on task"}
	    response = Response(json.dumps(error), mimetype='application/json')
	    return response
	    
if __name__ == "__main__":                
    app.run()