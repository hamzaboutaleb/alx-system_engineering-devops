#!/usr/bin/python3
"""Get user todos"""
import requests
import json
from requests.exceptions import HTTPError
from sys import argv


FILE_OUTPUT_NAME = "{}.json"


def get_user(id):
    """Get user by id"""
    response = requests.get(f"https://jsonplaceholder.typicode.com/users/{id}")
    if response.status_code != 200:
        raise HTTPError(f'HTTP Error: {response.status_code}')
    return response.json()


def get_todos_by_user_id(id):
    """Get User todos"""
    response = requests.get(f"https://jsonplaceholder.typicode.com/todos")
    if response.status_code != 200:
        raise HTTPError(f'HTTP Error: {response.status_code}')
    todos = response.json()
    result = []
    completed = []
    for todo in todos:
        if todo['userId'] == id:
            result.append(todo)
            if todo['completed']:
                completed.append(todo)
    return {
        'todos': result,
        'completed': completed
    }

def to_json_format(user, todos):
    id = user['id']
    username = user['username']
    result = {
        id: []
    }
    for todo in todos:
        todo_obj = {
            "task": todo['title'],
            "completed": todo['completed'],
            'username': username
        }
        result[id].append(todo_obj)

    return json.dumps(result)

def save_file(content, user_id):
    with open(FILE_OUTPUT_NAME.format(user_id), "w") as f:
        f.write(content)

def print_user_todos(user, todos):
    """print user todos"""
    text = "Employee {} is done with tasks({}/{}):\n"
    name = user['name']
    completed = todos['completed']
    todosList = todos['todos']
    result = text.format(name, len(completed), len(todosList))
    for todo in completed:
        result += f"\t {todo['title']}\n"
    print(result[0:-1])


def main():
    """entry point"""
    if len(argv) != 2:
        print("Usage: python3 0-gather_data_from_an_API.py ID ")
        exit()

    id = argv[1]

    try:
        id = int(id)
        user = get_user(id)
        todos = get_todos_by_user_id(id)
        json_format = to_json_format(user, todos['todos'])
        save_file(json_format, user['id'])
    except ValueError:
        print("id must be integer")
    except HTTPError:
        print("something went wrong")


if __name__ == "__main__":
    main()
