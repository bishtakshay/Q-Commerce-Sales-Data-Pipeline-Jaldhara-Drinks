import os
import csv

def remove_redundant_rows(INPUT_FILE):
    # Create folders safely (won't crash if they exist)
    os.makedirs("Output-files", exist_ok=True)
    os.makedirs("Dump-files", exist_ok=True)

    OUTPUT_FILE = os.path.join("Output-files", "BB-cleaned.csv")
    DUMP_FILE = os.path.join("Dump-files", "BB-duplicates.txt")

    seen_rows = set()
    rows_to_keep = []
    removed_entries = []
    total_data_rows = 0

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows_to_keep.append(header)

        for row in reader:
            if not row:
                continue

            total_data_rows += 1
            row_tuple = tuple(cell.strip() for cell in row)

            if row_tuple not in seen_rows:
                seen_rows.add(row_tuple)
                rows_to_keep.append(row)
            else:
                removed_entries.append(row)

    # Write cleaned file
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows_to_keep)

    # Write dump file
    with open(DUMP_FILE, "w", encoding="utf-8") as f:
        f.write("Redundant entries removed (duplicates)\n")
        f.write("=" * 80 + "\n")
        f.write(f"Header: {' | '.join(header)}\n")
        f.write("=" * 80 + "\n\n")

        for i, row in enumerate(removed_entries, 1):
            f.write(f"RE #{i}: {' | '.join(row)}\n")

    duplicates_removed = total_data_rows - (len(rows_to_keep) - 1)

    print(f"Read {INPUT_FILE}")
    print(f"Total data rows: {total_data_rows}")
    print(f"Duplicate rows removed: {duplicates_removed}")
    print(f"Written to {OUTPUT_FILE}")
    print(f"Removed entries listed in {DUMP_FILE}")


if __name__ == "__main__":
    remove_redundant_rows("BB-raw.csv")


import os
import csv

def split_date_column(INPUT_FILE):
    # Check if input file exists
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found!")
        print("Please run the previous script first to generate BB-cleaned.csv")
        return
    
    # Create output folder
    os.makedirs("Output-files", exist_ok=True)
    OUTPUT_FILE = os.path.join("Output-files", "BB-dates-split.csv")
    
    rows_processed = []
    
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        
        # Create new header with split date columns
        new_header = ["Starting Date", "Ending Date"] + header[1:]
        rows_processed.append(new_header)
        
        print(f"Original header: {header}")
        print(f"New header: {new_header}\n")
        
        for row_num, row in enumerate(reader, start=2):
            if not row:
                continue
            
            # Get the first column (date range)
            date_range = row[0].strip()
            
            # Split the date range
            # Common formats: "01/01/2024 - 01/31/2024", "01/01/2024-01/31/2024", "01/01/2024 to 01/31/2024"
            start_date = ""
            end_date = ""
            
            # Try different separators
            if " - " in date_range:
                parts = date_range.split(" - ")
                start_date = parts[0].strip()
                end_date = parts[1].strip() if len(parts) > 1 else ""
            elif " to " in date_range.lower():
                parts = date_range.lower().split(" to ")
                start_date = parts[0].strip()
                end_date = parts[1].strip() if len(parts) > 1 else ""
            elif "-" in date_range:
                parts = date_range.split("-")
                start_date = parts[0].strip()
                end_date = parts[1].strip() if len(parts) > 1 else ""
            else:
                # If no separator found, put entire value in start_date
                start_date = date_range
                end_date = ""
            
            # Create new row with split dates
            new_row = [start_date, end_date] + row[1:]
            rows_processed.append(new_row)
            
            # Show first few examples
            if row_num <= 5:
                print(f"Row {row_num}: '{date_range}' → Start: '{start_date}' | End: '{end_date}'")
    
    # Write the output file
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows_processed)
    
    print(f"\n✓ Processed {len(rows_processed) - 1} rows")
    print(f"✓ Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    INPUT_FILE = os.path.join("Output-files", "BB-cleaned.csv")
    split_date_column(INPUT_FILE)



import os
import csv
from datetime import datetime
from collections import defaultdict

def parse_date(date_string):
    """
    Try to parse date string in various formats.
    Returns datetime object or None if parsing fails.
    """
    date_string = date_string.strip()
    if not date_string:
        return None
    
    # Common date formats to try
    formats = [
         "%Y%m%d",      # 20240131  
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    
    return None

def sort_by_ending_date_monthwise(INPUT_FILE):
    # Check if input file exists
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found!")
        print("Please run the date-split script first.")
        return
    
    # Create output folder
    os.makedirs("Output-files", exist_ok=True)
    OUTPUT_FILE = os.path.join("Output-files", "BB-sorted-monthwise.csv")
    
    # Dictionary to group rows by year-month
    month_groups = defaultdict(list)
    unparseable_rows = []
    
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        
        print(f"Header: {header}\n")
        print("Processing rows and grouping by ending date month...\n")
        
        for row_num, row in enumerate(reader, start=2):
            if not row:
                continue
            
            # Get ending date (should be in column 1 after split)
            ending_date_str = row[1].strip() if len(row) > 1 else ""
            
            # Parse the ending date
            ending_date = parse_date(ending_date_str)
            
            if ending_date:
                # Create year-month key (YYYY-MM format for sorting)
                month_key = ending_date.strftime("%Y-%m")
                month_label = ending_date.strftime("%B %Y")  # e.g., "January 2024"
                
                # Store row with its parsed date for sorting within month
                month_groups[month_key].append({
                    'date': ending_date,
                    'date_str': ending_date_str,
                    'month_label': month_label,
                    'row': row
                })
                
                if row_num <= 5:
                    print(f"Row {row_num}: '{ending_date_str}' → Grouped in: {month_label}")
            else:
                unparseable_rows.append(row)
                print(f"⚠ Row {row_num}: Could not parse date '{ending_date_str}'")
    
    # Sort month groups (oldest to latest)
    sorted_months = sorted(month_groups.keys())
    
    # Prepare output rows
    output_rows = [header]
    
    print(f"\n{'='*80}")
    print("SORTED OUTPUT (Oldest to Latest):")
    print(f"{'='*80}\n")
    
    for month_key in sorted_months:
        entries = month_groups[month_key]
        
        # Sort entries within the month by date (oldest to latest)
        entries.sort(key=lambda x: x['date'])
        
        month_label = entries[0]['month_label']
        print(f"📅 {month_label} ({len(entries)} entries)")
        
        for entry in entries:
            output_rows.append(entry['row'])
    
    # Add unparseable rows at the end
    if unparseable_rows:
        print(f"\n⚠ Unparseable dates ({len(unparseable_rows)} entries) - added at end")
        output_rows.extend(unparseable_rows)
    
    # Write sorted output
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(output_rows)
    
    print(f"\n{'='*80}")
    print(f"✓ Total months processed: {len(sorted_months)}")
    print(f"✓ Total rows processed: {len(output_rows) - 1}")
    print(f"✓ Output saved to: {OUTPUT_FILE}")
    print(f"{'='*80}")


if __name__ == "__main__":
    INPUT_FILE = os.path.join("Output-files", "BB-dates-split.csv")
    sort_by_ending_date_monthwise(INPUT_FILE)




"""
Correct code above this 
"""



import os
import csv
from datetime import datetime
from collections import defaultdict

def parse_date(date_string):
    """
    Parse date string in YYYYMMDD format.
    Returns datetime object or None if parsing fails.
    """
    date_string = date_string.strip()
    if not date_string:
        return None
    
    # Only use YYYYMMDD format
    formats = [
        "%Y%m%d",      # 20240131  
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    
    return None

def keep_all_entries_for_last_date_per_month(INPUT_FILE):
    # Check if input file exists
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found!")
        print("Please run the date-split script first.")
        return
    
    # Create output folder
    os.makedirs("Output-files", exist_ok=True)
    OUTPUT_FILE = os.path.join("Output-files", "BB-last-date-entries-per-month.csv")
    
    # Dictionary to store all entries per month with their dates
    month_entries = defaultdict(list)
    unparseable_rows = []
    total_rows = 0
    parsed_count = 0
    
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        
        print(f"Header: {header}\n")
        print("Processing rows and grouping by month...\n")
        
        for row_num, row in enumerate(reader, start=2):
            if not row:
                continue
            
            total_rows += 1
            
            # Get ending date (should be in column 1 after split)
            ending_date_str = row[1].strip() if len(row) > 1 else ""
            
            # Parse the ending date
            ending_date = parse_date(ending_date_str)
            
            if ending_date:
                parsed_count += 1
                # Create year-month key (YYYY-MM format)
                month_key = ending_date.strftime("%Y-%m")
                month_label = ending_date.strftime("%B %Y")
                
                # Store all entries with their dates
                month_entries[month_key].append({
                    'date': ending_date,
                    'date_str': ending_date_str,
                    'month_label': month_label,
                    'row': row
                })
            else:
                unparseable_rows.append(row)
                if len(unparseable_rows) <= 5:
                    print(f"⚠ Row {row_num}: Could not parse date '{ending_date_str}'")
        
        if len(unparseable_rows) > 5:
            print(f"⚠ ... and {len(unparseable_rows) - 5} more unparseable dates")
    
    # For each month, find the latest date and keep ALL entries with that date
    month_last_date_entries = {}
    
    for month_key, entries in month_entries.items():
        # Find the maximum (latest) date in this month
        max_date = max(entry['date'] for entry in entries)
        
        # Keep ALL entries that have this maximum date
        last_date_entries = [entry for entry in entries if entry['date'] == max_date]
        
        month_last_date_entries[month_key] = {
            'max_date': max_date,
            'entries': last_date_entries,
            'count': len(last_date_entries)
        }
    
    # Sort months from oldest to latest
    sorted_months = sorted(month_last_date_entries.keys())
    
    # Prepare output rows
    output_rows = [header]
    
    print(f"\n{'='*80}")
    print("FINAL OUTPUT (All Entries for Last Date Per Month - Oldest to Latest):")
    print(f"{'='*80}\n")
    
    total_entries_kept = 0
    for i, month_key in enumerate(sorted_months, 1):
        month_data = month_last_date_entries[month_key]
        max_date = month_data['max_date']
        entries = month_data['entries']
        count = month_data['count']
        
        month_label = max_date.strftime("%B %Y")
        date_str = max_date.strftime("%Y%m%d")
        
        # Show first 10 and last 5 months
        if i <= 10 or i > len(sorted_months) - 5:
            print(f"📅 {month_label}: {date_str} ({count} entries)")
        elif i == 11:
            print(f"   ... ({len(sorted_months) - 15} more months) ...")
        
        # Add all entries for this month's last date
        for entry in entries:
            output_rows.append(entry['row'])
            total_entries_kept += 1
    
    # Add unparseable rows at the end (optional)
    if unparseable_rows:
        print(f"\n⚠ Unparseable dates ({len(unparseable_rows)} entries) - added at end")
        output_rows.extend(unparseable_rows)
    
    # Write output
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(output_rows)
    
    print(f"\n{'='*80}")
    print(f"📊 STATISTICS:")
    print(f"{'='*80}")
    print(f"Total rows processed: {total_rows}")
    print(f"Successfully parsed dates: {parsed_count}")
    print(f"Unparseable dates: {len(unparseable_rows)}")
    print(f"Total months found: {len(sorted_months)}")
    print(f"Total entries kept (all with last date): {total_entries_kept}")
    print(f"Rows in output: {len(output_rows) - 1}")
    print(f"Rows removed: {total_rows - (len(output_rows) - 1)}")
    print(f"\n✓ Output saved to: {OUTPUT_FILE}")
    print(f"{'='*80}")


if __name__ == "__main__":
    INPUT_FILE = os.path.join("Output-files", "BB-dates-split.csv")
    keep_all_entries_for_last_date_per_month(INPUT_FILE)