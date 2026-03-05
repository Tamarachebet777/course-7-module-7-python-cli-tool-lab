import argparse
import sys
import os

# Fix import so it works both as a module (python -m lib.cli_tool)
# and as a direct script (python cli_tool.py)
try:
    from lib.models import Task, User
except ModuleNotFoundError:
    from models import Task, User

# Global dictionary to store users and their tasks
users = {}


def add_task(args):
    # Check if the user exists, if not, create one
    if args.user not in users:
        users[args.user] = User(args.user)

    # Create a new Task with the given title
    task = Task(args.title)

    # Add the task to the user's task list
    users[args.user].add_task(task)


def complete_task(args):
    # Look up the user by name
    user = users.get(args.user)

    if user:
        # Look up the task by title
        task = user.get_task_by_title(args.title)

        if task:
            # Mark the task as complete
            task.complete()
        else:
            print(f"❌ Task '{args.title}' not found for user '{args.user}'.")
            pending = [t.title for t in user.tasks if not t.completed]
            if pending:
                print(f"   Available tasks: {', '.join(pending)}")
    else:
        print(f"❌ User '{args.user}' not found.")
        if users:
            print(f"   Known users: {', '.join(users.keys())}")


def main():
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers()

    # Subparser for adding tasks
    add_parser = subparsers.add_parser("add-task", help="Add a task for a user")
    add_parser.add_argument("user")
    add_parser.add_argument("title")
    add_parser.set_defaults(func=add_task)

    # Subparser for completing tasks
    complete_parser = subparsers.add_parser("complete-task", help="Complete a user's task")
    complete_parser.add_argument("user")
    complete_parser.add_argument("title")
    complete_parser.set_defaults(func=complete_task)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
    