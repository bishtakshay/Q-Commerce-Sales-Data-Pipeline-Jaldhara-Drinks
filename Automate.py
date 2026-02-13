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
    
    formats = ["%Y%m%d"]  # 20240131
    
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    
    return None


def process_bb_data(input_file, output_file):
    """
    Process BB data: remove duplicates, split date columns, and keep all entries 
    for the last date per month.
    
    Args:
        input_file: Path to the input CSV file (e.g., "BB-raw.csv")
        output_file: Path to the output CSV file (e.g., "BB-final.csv")
    
    Returns:
        dict: Statistics about the processing
    """
    
    # Validate input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Create output directory if needed
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    print(f"Processing {input_file}...")
    print("=" * 80)
    
    # STEP 1: Remove duplicates
    print("\n[Step 1/3] Removing duplicate rows...")
    seen_rows = set()
    unique_rows = []
    total_input_rows = 0
    duplicates_removed = 0
    
    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        unique_rows.append(header)
        
        for row in reader:
            if not row:
                continue
            
            total_input_rows += 1
            row_tuple = tuple(cell.strip() for cell in row)
            
            if row_tuple not in seen_rows:
                seen_rows.add(row_tuple)
                unique_rows.append(row)
            else:
                duplicates_removed += 1
    
    print(f"✓ Total input rows: {total_input_rows}")
    print(f"✓ Duplicates removed: {duplicates_removed}")
    print(f"✓ Unique rows: {len(unique_rows) - 1}")
    
    # STEP 2: Split date column
    print("\n[Step 2/3] Splitting date range column...")
    rows_with_split_dates = []
    
    # Create new header with split date columns
    new_header = ["Starting Date", "Ending Date"] + header[1:]
    rows_with_split_dates.append(new_header)
    
    for row in unique_rows[1:]:  # Skip header
        if not row:
            continue
        
        # Get the first column (date range)
        date_range = row[0].strip()
        
        # Split the date range
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
        rows_with_split_dates.append(new_row)
    
    print(f"✓ Date columns split: {len(rows_with_split_dates) - 1} rows processed")
    
    # STEP 3: Keep all entries for last date per month
    print("\n[Step 3/3] Filtering: keeping all entries for last date per month...")
    
    month_entries = defaultdict(list)
    unparseable_rows = []
    parsed_count = 0
    
    for row in rows_with_split_dates[1:]:  # Skip header
        if not row:
            continue
        
        # Get ending date (column 1 after split)
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
    
    # Prepare final output rows
    output_rows = [new_header]
    total_entries_kept = 0
    
    for month_key in sorted_months:
        month_data = month_last_date_entries[month_key]
        entries = month_data['entries']
        
        # Add all entries for this month's last date
        for entry in entries:
            output_rows.append(entry['row'])
            total_entries_kept += 1
    
    # Add unparseable rows at the end (optional)
    if unparseable_rows:
        output_rows.extend(unparseable_rows)
    
    print(f"✓ Months processed: {len(sorted_months)}")
    print(f"✓ Entries kept (last date per month): {total_entries_kept}")
    print(f"✓ Unparseable dates (added at end): {len(unparseable_rows)}")
    
    # Write final output file
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(output_rows)
    
    # Calculate statistics
    total_rows_removed = (len(unique_rows) - 1) - (len(output_rows) - 1)
    
    stats = {
        'input_file': input_file,
        'output_file': output_file,
        'total_input_rows': total_input_rows,
        'duplicates_removed': duplicates_removed,
        'unique_rows_after_dedup': len(unique_rows) - 1,
        'parsed_dates': parsed_count,
        'unparseable_dates': len(unparseable_rows),
        'total_months': len(sorted_months),
        'final_output_rows': len(output_rows) - 1,
        'total_rows_removed': total_rows_removed
    }
    
    print("\n" + "=" * 80)
    print("PROCESSING COMPLETE!")
    print("=" * 80)
    print(f"📊 STATISTICS:")
    print(f"  • Input rows: {stats['total_input_rows']}")
    print(f"  • Duplicates removed: {stats['duplicates_removed']}")
    print(f"  • Unique rows: {stats['unique_rows_after_dedup']}")
    print(f"  • Successfully parsed dates: {stats['parsed_dates']}")
    print(f"  • Unparseable dates: {stats['unparseable_dates']}")
    print(f"  • Months found: {stats['total_months']}")
    print(f"  • Final output rows: {stats['final_output_rows']}")
    print(f"  • Total rows filtered out: {stats['total_rows_removed']}")
    print(f"\n✓ Output saved to: {output_file}")
    print("=" * 80)
    
    return stats


if __name__ == "__main__":
    # Example usage
    process_bb_data("BB-raw.csv", "BB-final.csv")