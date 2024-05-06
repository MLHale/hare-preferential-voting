import pandas as pd
import re
import sys

def read_and_filter_qualtrics_data(file_path):
    # Load the CSV file into a DataFrame
    data = pd.read_csv(file_path)

    # Compile a regex pattern to match column names needed for the ballot. 
    # Qualtrics stores raw ballots in columns named Q*_0_GROUP to indicate the *th question and there is only 1 group (group 0)
    # pattern = re.compile(r'Q\d+_0_GROUP')

    # # Filter columns based on the regex pattern
    # matching_columns = [col for col in data.columns if pattern.match(col)]

    # Replace qualtrics question number with election name
    mapping = {'Q1_0_GROUP': 'Advisory(CS)', 'Q2_0_GROUP': 'Advisory(ISQA)', 'Q3_0_GROUP': 'Advisory(Si2)', 'Q4_0_GROUP': 'Academic(CS)', 'Q5_0_GROUP': 'Academic(ISQA)', 'Q6_0_GROUP': 'Academic(Si2)',  'Q7_0_GROUP': 'Personnel(CS)', 'Q8_0_GROUP': 'Personnel(ISQA)', 'Q9_0_GROUP': 'Personnel(Si2)', 'Q10_0_GROUP': 'Doctoral(CS)', 'Q11_0_GROUP': 'Doctoral(Si2)'}

    data.rename(columns=mapping, inplace=True)

    # remove qualtrics metadata in the 1st and 2nd rows
    data = data.drop([0, 1])

    # Filter data to only include the relevant columns (lists of ballots)
    matching_columns = [value for value in mapping.values()]

    return data[matching_columns]

def prepare_csv_for_hare(dataframe, output_file):
    # Open a file to write
    with open(output_file, 'w') as file:
        # Iterate over each column (each election)
        for column in dataframe.columns:
            # Extract the column data (ballots)
            ballots = dataframe[column].dropna().tolist()
            
            # The number of slots is usually 1, might need to customize this per ballot in unique circumstances (like replacements)
            num_slots = 1

            # the list of candidates is the same for all ballots, just take the first one:
            candidate_names = ballots[0]

            # Preamble structure: start, name of election, number of slots, candidate names
            preamble = 'start,{},{},{}'.format(column, num_slots,candidate_names)
            
            # Write the preamble
            file.write(preamble + '\n')
            
            # Write each ballot
            for ballot in ballots:
                file.write(ballot + '\n')
            
            # Write the 'end' line
            file.write('end\n')


if __name__ == "__main__":
    # Check if the user has provided a file path as an argument
    if len(sys.argv) < 3:
        print("Usage: python script_name.py path_to_qualtrics_export.csv output_election_file.csv")
        sys.exit(1)

    qualtrics_export_file_path = sys.argv[1]
    output_file = sys.argv[2]
    ballots = read_and_filter_qualtrics_data(qualtrics_export_file_path)
    # print(filtered_data)
    hare_ready_csv = prepare_csv_for_hare(ballots, output_file)
