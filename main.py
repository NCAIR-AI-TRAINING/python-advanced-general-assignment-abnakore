from datetime import datetime
import os

class DuplicateVisitorError(Exception):
    pass

class EarlyEntryError(Exception):
    pass

FILENAME = "visitors.txt"

def ensure_file():
    """Create file if it doesn't exist."""
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w") as f:
            pass

def get_last_visitor():
    """Return (name, timestamp) of last visitor or (None, None) if file is empty."""
    with open(FILENAME, "r") as f:
        lines = f.readlines()

    if not lines:
        return None, None

    # Get the name and timestamp of the last visitor
    name, timestamp = lines[-1].strip().split(" - ")
    return name, timestamp

def add_visitor(visitor_name):
    last_name, last_time = get_last_visitor()
    now = datetime.now()

    # Check duplicate consecutive visitor
    if last_name == visitor_name:
        raise DuplicateVisitorError(f"'{visitor_name}' cannot sign in twice in a row.")

    # Log visitor
    with open(FILENAME, "a") as f:
        f.write(f"{visitor_name} - {now.strftime('%d/%m/%Y %H:%M:%S')}\n")

def main():
    ensure_file()
    name = input("Enter visitor's name: ")
    try:
        add_visitor(name)
        print("Visitor added successfully!")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
