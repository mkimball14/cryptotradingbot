#!/usr/bin/env python3
import json
import re
import sys
import os
import gzip
from collections import Counter, defaultdict
from datetime import datetime
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Analyze WebSocket log files to extract key information')
    parser.add_argument('log_file', help='Path to the WebSocket log file')
    parser.add_argument('--output', '-o', help='Path to save the analysis results', default='log_analysis.txt')
    parser.add_argument('--sample', '-s', type=int, help='Number of sample messages to save per type', default=2)
    parser.add_argument('--errors-only', '-e', action='store_true', help='Only analyze error messages')
    parser.add_argument('--time-range', '-t', help='Analyze only logs within time range (format: HH:MM-HH:MM)')
    return parser.parse_args()

def read_log_file(file_path, time_range=None):
    """Read and yield lines from a log file, optionally filtering by time range"""
    # Check if file is gzipped
    is_gzipped = file_path.endswith('.gz')
    opener = gzip.open if is_gzipped else open
    mode = 'rt' if is_gzipped else 'r'
    
    # Parse time range if provided
    start_time, end_time = None, None
    if time_range:
        try:
            start_str, end_str = time_range.split('-')
            start_time = datetime.strptime(start_str.strip(), '%H:%M')
            end_time = datetime.strptime(end_str.strip(), '%H:%M')
        except ValueError:
            print(f"Invalid time range format: {time_range}. Using format HH:MM-HH:MM")
            time_range = None
    
    print(f"Reading log file: {file_path}")
    file_size = os.path.getsize(file_path)
    if file_size > 1024*1024*100:  # If file is larger than 100MB
        print(f"Large file detected ({file_size / (1024*1024):.1f} MB). Processing may take some time...")
    
    line_count = 0
    processed_lines = 0
    
    try:
        with opener(file_path, mode) as f:
            for line in f:
                line_count += 1
                
                # Status update every million lines
                if line_count % 1000000 == 0:
                    print(f"Processed {line_count} lines...")
                
                # Filter by time range if specified
                if time_range:
                    # Extract timestamp from log line (assuming format like "2023-06-07 14:23:45")
                    timestamp_match = re.search(r'\d{4}-\d{2}-\d{2} (\d{2}:\d{2}):\d{2}', line)
                    if timestamp_match:
                        line_time_str = timestamp_match.group(1)
                        line_time = datetime.strptime(line_time_str, '%H:%M')
                        
                        # Check if time is within range
                        if start_time <= end_time:  # Normal range (e.g., 09:00-17:00)
                            if not (start_time <= line_time <= end_time):
                                continue
                        else:  # Overnight range (e.g., 22:00-06:00)
                            if not (line_time >= start_time or line_time <= end_time):
                                continue
                
                processed_lines += 1
                yield line
    
    except Exception as e:
        print(f"Error reading log file: {str(e)}")
        return
        
    print(f"Finished reading {line_count} total lines ({processed_lines} processed)")

def extract_json_objects(line):
    """Extract JSON objects from a log line"""
    json_objects = []
    
    # Find potential JSON objects in the line
    json_pattern = r'({.*?})'
    json_matches = re.findall(json_pattern, line)
    
    for potential_json in json_matches:
        try:
            json_obj = json.loads(potential_json)
            if isinstance(json_obj, dict):
                json_objects.append(json_obj)
        except json.JSONDecodeError:
            # Try to find nested JSON objects that might be stringified
            try:
                # Look for escaped JSON strings within the object
                nested_jsons = re.findall(r'"({.*?})"', potential_json)
                for nested_json in nested_jsons:
                    try:
                        # Unescape the string and try to parse
                        cleaned = nested_json.replace('\\"', '"')
                        nested_obj = json.loads(cleaned)
                        if isinstance(nested_obj, dict):
                            json_objects.append(nested_obj)
                    except json.JSONDecodeError:
                        continue
            except:
                pass
    
    return json_objects

def analyze_websocket_log(log_file, errors_only=False, sample_count=2, time_range=None):
    """Analyze WebSocket log file and extract key information"""
    # Statistics
    message_types = Counter()
    message_channels = Counter()
    error_messages = []
    subscription_messages = []
    connection_events = []
    time_series_data = defaultdict(int)
    sample_messages = defaultdict(list)
    
    # Track authentication
    auth_attempts = 0
    auth_successes = 0
    
    # Process log file
    for line in read_log_file(log_file, time_range):
        # Track connection events
        if "CONNECTED to WebSocket" in line:
            timestamp = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
            if timestamp:
                connection_events.append(f"Connected: {timestamp.group(1)}")
        
        if "DISCONNECTED from WebSocket" in line:
            timestamp = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
            if timestamp:
                connection_events.append(f"Disconnected: {timestamp.group(1)}")
        
        # Extract JSON objects from line
        json_objects = extract_json_objects(line)
        
        # Skip non-JSON lines if we're only interested in errors
        if errors_only and not json_objects and "ERROR" not in line:
            continue
        
        # Process non-JSON error lines
        if "ERROR" in line and not any("error" in obj.get("type", "").lower() for obj in json_objects):
            error_messages.append(line.strip())
        
        # Process JSON objects
        for json_obj in json_objects:
            # Extract timestamp for time series (if available)
            timestamp = json_obj.get("timestamp")
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    hour_key = dt.strftime('%Y-%m-%d %H')
                    time_series_data[hour_key] += 1
                except (ValueError, TypeError):
                    pass
            
            # Track message type
            msg_type = json_obj.get("type")
            if msg_type:
                message_types[msg_type] += 1
                
                # Collect sample messages
                if len(sample_messages[msg_type]) < sample_count:
                    sample_messages[msg_type].append(json_obj)
            
            # Track channel
            channel = json_obj.get("channel")
            if channel:
                message_channels[channel] += 1
            
            # Track errors
            if msg_type == "error" or "error" in json_obj:
                error_text = json.dumps(json_obj, indent=2)
                error_messages.append(error_text)
            
            # Track subscriptions
            if msg_type == "subscribe" or msg_type == "unsubscribe" or msg_type == "subscriptions":
                subscription_messages.append(json_obj)
            
            # Track authentication
            if msg_type == "auth":
                auth_attempts += 1
                status = json_obj.get("success", False)
                if status:
                    auth_successes += 1
    
    return {
        "message_types": message_types,
        "message_channels": message_channels,
        "error_messages": error_messages,
        "subscription_messages": subscription_messages,
        "connection_events": connection_events,
        "time_series_data": time_series_data,
        "sample_messages": sample_messages,
        "auth_attempts": auth_attempts,
        "auth_successes": auth_successes
    }

def generate_report(analysis_results, output_file):
    """Generate a report from the analysis results"""
    with open(output_file, 'w') as f:
        # Write header
        f.write("=" * 80 + "\n")
        f.write("WebSocket Log Analysis Report\n")
        f.write("=" * 80 + "\n\n")
        
        # Write summary
        f.write("SUMMARY\n")
        f.write("-" * 80 + "\n")
        
        total_messages = sum(analysis_results["message_types"].values())
        f.write(f"Total Messages: {total_messages}\n")
        f.write(f"Unique Message Types: {len(analysis_results['message_types'])}\n")
        f.write(f"Unique Channels: {len(analysis_results['message_channels'])}\n")
        f.write(f"Error Messages: {len(analysis_results['error_messages'])}\n")
        f.write(f"Connection Events: {len(analysis_results['connection_events'])}\n")
        f.write(f"Authentication Attempts: {analysis_results['auth_attempts']}\n")
        f.write(f"Authentication Successes: {analysis_results['auth_successes']}\n\n")
        
        # Write message types
        f.write("MESSAGE TYPES\n")
        f.write("-" * 80 + "\n")
        for msg_type, count in analysis_results["message_types"].most_common():
            percentage = (count / total_messages) * 100 if total_messages > 0 else 0
            f.write(f"{msg_type}: {count} ({percentage:.2f}%)\n")
        f.write("\n")
        
        # Write message channels
        f.write("MESSAGE CHANNELS\n")
        f.write("-" * 80 + "\n")
        for channel, count in analysis_results["message_channels"].most_common():
            percentage = (count / total_messages) * 100 if total_messages > 0 else 0
            f.write(f"{channel}: {count} ({percentage:.2f}%)\n")
        f.write("\n")
        
        # Write connection events
        f.write("CONNECTION EVENTS\n")
        f.write("-" * 80 + "\n")
        for event in analysis_results["connection_events"]:
            f.write(f"{event}\n")
        f.write("\n")
        
        # Write time series data
        f.write("MESSAGE VOLUME BY HOUR\n")
        f.write("-" * 80 + "\n")
        for hour, count in sorted(analysis_results["time_series_data"].items()):
            f.write(f"{hour}: {count}\n")
        f.write("\n")
        
        # Write sample messages
        f.write("SAMPLE MESSAGES BY TYPE\n")
        f.write("-" * 80 + "\n")
        for msg_type, samples in analysis_results["sample_messages"].items():
            f.write(f"\n{msg_type.upper()} SAMPLES:\n")
            for i, sample in enumerate(samples):
                f.write(f"Sample {i+1}:\n")
                f.write(json.dumps(sample, indent=2) + "\n")
        f.write("\n")
        
        # Write subscription messages
        f.write("SUBSCRIPTION MESSAGES\n")
        f.write("-" * 80 + "\n")
        for msg in analysis_results["subscription_messages"]:
            f.write(json.dumps(msg, indent=2) + "\n\n")
        f.write("\n")
        
        # Write error messages
        f.write("ERROR MESSAGES\n")
        f.write("-" * 80 + "\n")
        for error in analysis_results["error_messages"]:
            f.write(f"{error}\n\n")
    
    print(f"Analysis report saved to {output_file}")

if __name__ == "__main__":
    args = parse_arguments()
    
    if not os.path.exists(args.log_file):
        print(f"Error: Log file '{args.log_file}' not found")
        sys.exit(1)
    
    print("Starting WebSocket log analysis...")
    analysis_results = analyze_websocket_log(
        args.log_file, 
        errors_only=args.errors_only, 
        sample_count=args.sample,
        time_range=args.time_range
    )
    
    generate_report(analysis_results, args.output)
    print("Analysis complete!") 