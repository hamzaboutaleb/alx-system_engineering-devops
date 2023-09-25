#!/usr/bin/python3
"""Get user todos"""
import json
import requests
from requests.exceptions import HTTPError
from sys import argv


FILE_OUTPUT_NAME = "todo_all_employees.json"


def get_users():
    """Get user by id"""
    response = requests.get(f"https://jsonplaceholder.typicode.com/users")
    if response.status_code != 200:
        raise HTTPError(f'HTTP Error: {response.status_code}')
    return response.json()


def get_user(id):
    """Get user by id"""
    response = requests.get(f"https://jsonplaceholder.typicode.com/users/{id}")
    if response.status_code != 200:
        raise HTTPError(f'HTTP Error: {response.status_code}')
    return response.json()


def get_todos():
    """Get User todos"""
    response = requests.get(f"https://jsonplaceholder.typicode.com/todos")
    if response.status_code != 200:
        raise HTTPError(f'HTTP Error: {response.status_code}')
    todos = response.json()
    return todos


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


def to_json_format_all_users(users, todos):
    result = build_users_dict(users)
    lookup_username = build_lookup_users(users)
    for todo in todos:
        id = todo['userId']
        username = lookup_username[id]
        todo_obj = {
            'username': username,
            'task': todo['title'],
            'completed': todo['completed']
        }
        result[id].append(todo_obj)

    return json.dumps(result)


def build_lookup_users(users):
    result = {}
    for user in users:
        result[user['id']] = user['username']

    return result


def build_users_dict(users):
    result = {}
    for user in users:
        result[user["id"]] = []

    return result


def save_file(content):
    with open(FILE_OUTPUT_NAME, "w") as f:
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

    try:
        user = get_users()
        todos = get_todos()
        json_format = to_json_format_all_users(user, todos)
        save_file(json_format)
    except ValueError:
        print("id must be integer")
    except HTTPError:
        print("something went wrong")


if __name__ == "__main__":
    main()
