import os
import sys
from db import initialize_db, store_file_metadata, get_oldest_files, update_file_status
from file_scan import get_file_metadata, filter_top_files_by_date_or_size

def prompt_user_for_action(files_batch, offset):
    print("\nFiles for review:")
    for i, file in enumerate(files_batch, start=offset + 1):  # Use offset directly for global numbering
        print(f"{i}. File: {file[0]}, Size: {file[1]} bytes, Date Created: {file[2]}")

    while True:
        choice = input(
            "\nChoose files to mark for deletion (e.g., '1,3,5'), 'exit' to quit, or press Enter to skip: "
        ).strip()

        if choice.lower() == 'exit':  # If the user wants to quit the program
            print("Exiting the program.")
            sys.exit()

        if not choice:  # Skip the current batch if no choice is made
            print("Skipping this batch...")
            return [], "skip"

        try:
            selected_indices = [int(x.strip()) - 1 for x in choice.split(",")]
            if all(0 <= idx < len(files_batch) for idx in selected_indices):
                return [files_batch[idx] for idx in selected_indices], "delete"
            else:
                print("Invalid selection. Please choose numbers within the list range.")
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas.")

def main():
    # Step 1: Initialize the database
    initialize_db()

    # Step 2: Prompt user for a valid directory to scan or cancel
    while True:
        directory = input("Enter the directory to scan for media files (or type 'exit' to cancel): ").strip()
        if directory.lower() == 'exit':  # Check if user wants to cancel
            print("Exiting the program.")
            sys.exit()  # Exit the program immediately
        elif os.path.isdir(directory):
            break  # Valid directory entered, exit the loop
        else:
            print(f"Error: '{directory}' is not a valid directory. Please try again.")

    # Step 3: Prompt user for sorting preference
    while True:
        print("\nHow would you like to sort the files?")
        print("1. By size")
        print("2. By date created")
        print("3. By both date and size")
        sort_option = input("Enter your choice (1, 2, or 3): ").strip()

        if sort_option in {'1', '2', '3'}:
            break
        print("Invalid choice. Please enter 1, 2, or 3.")

    # Step 4: Get metadata for files in the directory
    files = get_file_metadata(directory)

    # Step 5: Filter top 500 files based on user preference
    if sort_option == '1':  # By size
        filtered_files = filter_top_files_by_date_or_size(files, count=500, sort_by='size')
    elif sort_option == '2':  # By date created
        filtered_files = filter_top_files_by_date_or_size(files, count=500, sort_by='date')
    else:  # By both (size first, then date for tie-breaking)
        filtered_files = filter_top_files_by_date_or_size(files, count=500, sort_by='both')

    # Step 6: Store metadata in the database
    for file in filtered_files:
        store_file_metadata(file[0], file[1], file[2], status=0)  # Unseen status

    # Step 7: Batch review and update status
    print("\nStored top 500 files in the database. Starting batch review of 20 files each.")
    batch_size = 20
    offset = 0  # Start with the first batch

    while True:
        # Fetch the next batch of unseen files
        batch = get_oldest_files(batch_size=batch_size, offset=offset, status=0)
        if not batch:
            print("\nNo more unseen files to review.")
            break

        # Prompt the user to review the current batch
        selected_files, action = prompt_user_for_action(batch, offset)

        if action == "delete":
            for file in selected_files:
                update_file_status(file[0], 1)  # Mark for deletion
            print("Marked selected files for deletion.")
            removed_files = selected_files
        else:
            removed_files = []

            # Mark current batch as skipped
            for file in batch:
                update_file_status(file[0], 2)  # Skip current batch
            print("Marked current batch as skipped.")

        # Display the files marked for deletion
        if removed_files:
            print("\nFiles marked for deletion in this batch:")
            for file in removed_files:
                print(f"File: {file[0]}, Size: {file[1]} bytes, Date Created: {file[2]}")
        else:
            print("\nNo files were marked for deletion in this batch.")

        offset += batch_size  # Move to the next batch

    print("\nReview complete. You can now process the marked files for deletion later.")

    # Exit the program
    sys.exit()

if __name__ == "__main__":
    main()
