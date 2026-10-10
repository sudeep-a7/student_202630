
import sys
import json
import csv


def parse_arguments():
    """Read the input and output filenames."""
    if len(sys.argv) < 2:
        print("Usage: python task_flattener.py input.json [output.csv]")
        sys.exit(1)

    input_file = sys.argv[1]

    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        output_file = "flattened_tasks.csv"

    return input_file, output_file


def flatten_tasks(tasks):
    """Flatten nested tasks into a single list."""
    flattened = []

    for task in tasks:
        # Copy the current task without its subtasks
        flat_task = {
            key: value
            for key, value in task.items()
            if key != "sub_tasks"
        }

        flattened.append(flat_task)

        # Recursively flatten the subtasks
        sub_tasks = task.get("sub_tasks", [])

        if sub_tasks:
            flattened.extend(flatten_tasks(sub_tasks))

    return flattened


def read_json(input_file):
    """Read tasks from a JSON file."""
    with open(input_file, "r", encoding="utf-8") as file:
        return json.load(file)


def save_csv(tasks, output_file):
    """Save flattened tasks to a CSV file."""
    if not tasks:
        raise ValueError("The task list is empty. Nothing to save.")

    # Use the task fields as CSV column headings
    fieldnames = tasks[0].keys()

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tasks)


def print_summary(tasks):
    """Print a summary of the flattened tasks."""
    print(f"Total tasks: {len(tasks)}")

    for task in tasks:
        details = task.get("details", "No description")
        status = task.get("status", "Unknown")
        assignee = task.get("assignee", "Unassigned")

        print(f"{details}, {status}, {assignee}")


def main():
    input_file, output_file = parse_arguments()

    try:
        tasks = read_json(input_file)

        if not isinstance(tasks, list):
            print("Error: The JSON file must contain a list of tasks.")
            return

        flattened = flatten_tasks(tasks)

        if not flattened:
            raise ValueError("The task list is empty.")

        print_summary(flattened)
        save_csv(flattened, output_file)

        print(f"Flattened tasks saved to '{output_file}'.")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        print(
            "Please run 'python generate_sample_data.py' first "
            "to create the input file"
        )

    except json.JSONDecodeError:
        print(f"Error: File '{input_file}' does not contain valid JSON.")

    except ValueError as error:
        print(f"Error: {error}")

    except OSError as error:
        print(f"Error reading or writing file: {error}")


if __name__ == "__main__":
    main()
