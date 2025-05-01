import re
import os

def process_two_log_files(file_path1, file_path2):
    """Process two log files and calculate timestamp differences between matching events"""
    # Regular expression pattern to extract timestamp, frame, slot, and event
    pattern = re.compile(r"\[(\d+\.\d+)\] frame=(\d+) slot=(\d+) (\w+.*)")
    
    # Dictionaries to store events from each file
    events_file1 = {}
    events_file2 = {}
    
    # Process first file
    print(f"Processing file 1: {os.path.basename(file_path1)}")
    try:
        with open(file_path1, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                match = pattern.match(line.strip())
                match = pattern.match(line.strip())
                if match:
                    timestamp, frame, slot, _ = match.groups()  # Use _ for unused variable
                    key = (int(frame), int(slot))
                    events_file1[key] = float(timestamp)
                if line_num % 1_000_000 == 0:
                    print(f"File 1: Processed {line_num//1_000_000} million lines...")
    except FileNotFoundError:
        print(f"Error: File {file_path1} not found")
        return None, None
    except Exception as e:
        print(f"Parsing error in file 1 (line {line_num}): {str(e)}")
        return None, None
    
    # Process second file
    print(f"Processing file 2: {os.path.basename(file_path2)}")
    try:
        with open(file_path2, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                match = pattern.match(line.strip())
                match = pattern.match(line.strip())
                if match:
                    timestamp, frame, slot, _ = match.groups()  # Use _ for unused variable
                    key = (int(frame), int(slot))
                    events_file2[key] = float(timestamp)
                if line_num % 1_000_000 == 0:
                    print(f"File 2: Processed {line_num//1_000_000} million lines...")
    except FileNotFoundError:
        print(f"Error: File {file_path2} not found")
        return None, None
    except Exception as e:
        print(f"Parsing error in file 2 (line {line_num}): {str(e)}")
        return None, None
    
    print(f"Found {len(events_file1)} events in file 1")
    print(f"Found {len(events_file2)} events in file 2")
    
    # Find common keys (frame, slot pairs) that exist in both files
    common_keys = set(events_file1.keys()) & set(events_file2.keys())
    print(f"Found {len(common_keys)} matching frame/slot pairs between the two files")
    # Calculate time differences
    # Calculate time differences
    diffs = []
    for key in common_keys:
        timestamp1 = events_file1[key]
        timestamp2 = events_file2[key]
        
        # Calculate time difference in seconds
        diff = timestamp2 - timestamp1
        diffs.append(abs(diff))  # Store absolute difference
    
    total = len(diffs)
    # Calculate average in seconds then convert to ms
    if total > 0:
        # Use high precision for the calculation to avoid floating point errors
        average = (sum(diffs) / total) * 1000
        if average == 0 and sum(diffs) > 0:  # If average is zero but there are differences
            # Force at least some precision to show
            average = (sum(diffs) / total) * 1000000 / 1000  # Convert to microseconds then back to ms
    else:
        average = 0
    return total, average

if __name__ == "__main__":
    file_path1 = input("Enter first log file path: ").strip()
    file_path2 = input("Enter second log file path: ").strip()
    
    # Remove surrounding double quotes if present
    if file_path1.startswith('"') and file_path1.endswith('"'):
        file_path1 = file_path1[1:-1]
    
    if file_path2.startswith('"') and file_path2.endswith('"'):
        file_path2 = file_path2[1:-1]
    
    if not os.path.isfile(file_path1):
        print(f"Error: Invalid file path for file 1: {file_path1}")
    elif not os.path.isfile(file_path2):
        print(f"Error: Invalid file path for file 2: {file_path2}")
    else:
        print(f"Analyzing files:")
        print(f"1. {os.path.basename(file_path1)}")
        print(f"2. {os.path.basename(file_path2)}")
        
        total, avg = process_two_log_files(file_path1, file_path2)
        
        if total is not None:
            print(f"\nFinal Results:")
            print(f"Valid matching pairs: {total}")
            print(f"Average time difference between files: {avg:.6f} ms")
            print(f"File 1 size: {os.path.getsize(file_path1)/1024/1024:.2f} MB")
            print(f"File 2 size: {os.path.getsize(file_path2)/1024/1024:.2f} MB")