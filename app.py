import os
from db import initialize_db, store_file_metadata
from file_scan import get_file_metadata, filter_top_files_by_date_or_size

def main():
    # Step 1: Initialize the database
    initialize_db()

    # Step 2: Prompt user for a valid directory to scan
    while True:
        directory = input("Enter the directory to scan for media files: ").strip()
        if os.path.isdir(directory):
            break
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

    # Step 5: Filter files based on user preference
    if sort_option == '1':  # By size
        filtered_files = filter_top_files_by_date_or_size(files, count=20, sort_by='size')
    elif sort_option == '2':  # By date created
        filtered_files = filter_top_files_by_date_or_size(files, count=20, sort_by='date')
    else:  # By both (size first, then date for tie-breaking)
        filtered_files = filter_top_files_by_date_or_size(files, count=20, sort_by='both')

    # Step 6: Store metadata in the database and display files to the user
    print("\nSelected files:")
    for i, file in enumerate(filtered_files, start=1):
        print(f"{i}. File: {file[0]}, Size: {file[1]} bytes, Date Created: {file[2]}")
        store_file_metadata(file[0], file[1], file[2])

    # Step 7: Allow the user to review files
    print("\nReview the files and decide whether to delete them.")

if __name__ == "__main__":
    main()
