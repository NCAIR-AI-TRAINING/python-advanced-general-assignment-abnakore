from datetime import datetime
import os

class DuplicateVisitorError(Exception):
    pass

class EarlyEntryError(Exception):
    pass

FILENAME = "visitors.txt"
WAIT_TIME_SECONDS = 5 * 60 # 5 minutes

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
    name, timestamp = lines[-1].strip().split(" | ")
    last_time = datetime.fromisoformat(timestamp)
    return name, last_time

def add_visitor(visitor_name):
    last_name, last_time = get_last_visitor()
    now = datetime.now()

    # Check duplicate consecutive visitor
    if last_name == visitor_name:
        raise DuplicateVisitorError(f"'{visitor_name}' cannot sign in twice in a row.")
    
    # Check 5-minute waiting rule
    if last_time is not None:
        elapsed = (now - last_time).total_seconds()
        if elapsed < WAIT_TIME_SECONDS:
            remaining = int(WAIT_TIME_SECONDS - elapsed)
            raise EarlyEntryError(f"Please wait {remaining // 60} min {remaining % 60} sec before logging the next visitor.")


    # Log visitor
    with open(FILENAME, "a") as f:
        f.write(f"{visitor_name} | {now.isoformat()}\n")

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
