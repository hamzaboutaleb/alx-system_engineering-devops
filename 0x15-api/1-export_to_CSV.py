#!/usr/bin/python3
"""Get user todos"""
import requests
from requests.exceptions import HTTPError
from sys import argv


FILE_OUTPUT_NAME = "USER_ID.csv"


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


def to_csv_format(user, todos):
    result = ""
    text = '"{}","{}","{}","{}"\n'
    for todo in todos:
        result += text.format(user['id'], user['username'],
                              todo['completed'], todo['title'])
    return result[0: -1]


def save_to_csv_file(content):
    with open(FILE_OUTPUT_NAME, "w") as f:
        f.write(content)


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
        csv_format = to_csv_format(user, todos['todos'])
        save_to_csv_file(csv_format)
    except ValueError:
        print("id must be integer")
    except HTTPError:
        print("something went wrong")


if __name__ == "__main__":
    main()
