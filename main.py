


INPUT_FILE = str(input("Enter the name of the input file: "))
OUTPUT_FILE = "BB-DRemoved.csv"
DUMP_FILE = "Removed-entries.txt"



from Automate import remove_redundant_rows
remove_redundant_rows(INPUT_FILE)




