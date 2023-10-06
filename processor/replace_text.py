import os

input_file = 'input/replace_text/input.txt'
output_file = 'output/replace_text/output.txt'

# Create folder if not exist
output_folder_path = 'output/replace_text/'
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)


def run(data: dict):

    with open(input_file, 'r') as file:
        filedata = file.read()

    for key, value in data.items():
        # Replace the target string
        filedata = filedata.replace('{{' + key + '}}', value)

    # Write the file out again
    with open(output_file, 'w') as file:
        file.write(filedata)
