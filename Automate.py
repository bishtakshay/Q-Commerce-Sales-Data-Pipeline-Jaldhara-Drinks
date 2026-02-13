"""
Remove redundant (exact duplicate) rows from BB-raw.csv.
Reads BB-raw.csv, keeps all unique rows (drops only exact duplicates),
and writes the result to a new file. Original file is not modified.
"""

import csv

INPUT_FILE = "BB-raw.csv"
OUTPUT_FILE = "BB-DRemoved.csv"
DUMP_FILE = "Removed-entries.txt"


def remove_redundant_rows():
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

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows_to_keep)

    # Write dump file: list of redundant entries that were removed
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
    print(f"Written to {OUTPUT_FILE} ({len(rows_to_keep) - 1} unique data rows + header)")
    print(f"Removed entries listed in {DUMP_FILE}")


if __name__ == "__main__":
    remove_redundant_rows()
