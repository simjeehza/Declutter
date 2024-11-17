import os
from datetime import datetime

def get_file_metadata(directory):
    """Search for media files and extract metadata."""
    media_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.jpg', '.png', '.mp4')):  # Supported file types
                file_path = os.path.join(root, file)
                file_stats = os.stat(file_path)
                size = file_stats.st_size
                date_created = datetime.utcfromtimestamp(file_stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
                media_files.append((file_path, size, date_created))
    return media_files

def filter_top_files_by_date_or_size(files, count=20, sort_by='date'):
    """
    Filters the top `count` files by size, date, or both.

    Args:
        files (list): List of tuples (path, size, date_created).
        count (int): Number of files to return.
        sort_by (str): Sorting criteria ('size', 'date', or 'both').

    Returns:
        list: Top `count` files sorted by the specified criteria.
    """
    if sort_by == 'size':
        # Sort by file size (largest first)
        sorted_files = sorted(files, key=lambda x: x[1], reverse=True)
    elif sort_by == 'date':
        # Sort by creation date (oldest first)
        sorted_files = sorted(files, key=lambda x: x[2])
    elif sort_by == 'both':
        # Sort by size (largest first), then by date (oldest first) as a tiebreaker
        sorted_files = sorted(files, key=lambda x: (-x[1], x[2]))
    else:
        raise ValueError("Invalid sort_by value. Use 'size', 'date', or 'both'.")

    return sorted_files[:count]
