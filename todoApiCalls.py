"""
requests is a library that simplifies making http requests using Python
url: http://docs.python-requests.org/en/latest/

installation: pip install requests
"""
import requests, sys

url = 'http://jsonplaceholder.typicode.com/todos'

def get_todos():
    """
    Get the 200 most recent TODOs.
    'python todoApiCalls get'
    """
    global url
    payload = {"_sort": "id", "_order": "desc"} #sort by id desc, since there is no created_at field
    response = requests.get(url, params=payload)
    return response.text

#Create a TODO
def create_todo(user_id, title, completed):
    """
    Create a TODO.
    'python todoApiCalls create ::user_id:: ::title:: ::completed::'
    """
    global url
    data = {"userId":user_id, "title":title, "completed": completed}
    response = requests.post(url, data=data)
    return response.status_code

def delete_todo(id):
    """
    Delete a TODO by id.
    'python todoApiCalls delete ::todo_id::'
    """
    global url
    response = requests.delete(url + "/" + id)
    return response.status_code


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception("Missing arguments: Please see the documentation for the proper way to use this script.")
    command = sys.argv[1]
    args = sys.argv[2:]

    if command == "get":
        result = get_todos()
    elif command == "create":
        if len(args) < 3:
            raise Exception("Missing arguments: Creating a TODO requires user_id, title, and completed.")
        user_id, title, completed = args[0], args[1], args[2]
        result = create_todo(user_id, title, completed)
    elif command == "delete":
        if len(args) < 1:
            raise Exception("Missing argument: Deleting a TODO requires todo_id")
        result = delete_todo(args[0])
    else:
        raise Exception("Invalid command: "+command+". Valid commands are: get, create, delete")
    print(result)