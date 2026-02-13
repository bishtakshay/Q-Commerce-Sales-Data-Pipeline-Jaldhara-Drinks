"""
Example main file demonstrating how to use the BB data processor
"""

from Automate import process_bb_data


def main():
    """
    Main function to process BB data files
    """
    
    # Define input and output file paths
    input_file = "BB-raw.csv"
    output_file = "Output-files/BB-final.csv"
    
    # Alternative: you can also use different paths
    # input_file = "path/to/your/BB-raw.csv"
    # output_file = "path/to/output/BB-final.csv"
    
    try:
        # Call the processing function
        stats = process_bb_data(input_file, output_file)
        
        # You can use the returned statistics for further processing
        print("\n📈 Processing Summary:")
        print(f"   Input: {stats['input_file']}")
        print(f"   Output: {stats['output_file']}")
        print(f"   Reduction: {stats['total_rows_removed']} rows filtered")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("   Please ensure the input file exists.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()