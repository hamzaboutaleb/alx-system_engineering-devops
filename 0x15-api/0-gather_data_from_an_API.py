#!/usr/bin/python3
import requests
from requests.exceptions import HTTPError
from sys import argv



def get_user(id):
  response = requests.get(f"https://jsonplaceholder.typicode.com/users/{id}")
  if response.status_code != 200:
    raise HTTPError(f'HTTP Error: {response.status_code}')
  return response.json()

def get_todos_by_user_id(id):
  response = requests.get(f"https://jsonplaceholder.typicode.com/todos")
  if response.status_code != 200:
    raise HTTPError(f'HTTP Error: {response.status_code}')
  todos = response.json()
  result = []
  completed = 0;
  for todo in todos:
    if todo['userId'] == id:
      result.append(todo)
      if todo['completed'] == True:
        completed += 1
  return {
    'todos': result,
    'completed': completed
  }

def print_user_todos(user, todos):
  result = f"Employee {user['name']} is done with tasks\
({str(todos['completed'])}/{len(todos['todos'])}):\n"
  for todo in todos['todos']:
    if todo['completed']:
      result += f"\t{todo['title']}\n"
  
  print(result)


def main():
  if len(argv) != 2:
    print("Usage: python3 0-gather_data_from_an_API.py ID ")
    exit()

  id = argv[1]

  try:
    id = int(id)
    user = get_user(id)
    todos = get_todos_by_user_id(id)
    print_user_todos(user, todos)
  except ValueError:
    print("id must be integer")
  except HTTPError:
    print("something went wrong")
  

if __name__ == "__main__":
  main()