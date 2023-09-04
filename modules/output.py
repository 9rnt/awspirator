import json
import csv

def write_dict_to_csv(file_path, data):
    try:
        with open(file_path, 'w', newline='') as csv_file:
            fieldnames = data[0].keys() if data else []
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
            for row in data:
                csv_writer.writerow(row)
        print(f'Data successfully written to {file_path}')
    except Exception as e:
        print(f'Error writing to {file_path}: {str(e)}')


def write_to_json_file(file_path, data):
    try:
    
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4) 
        print(f'Data successfully written to {file_path}')
    except Exception as e:
        print(f'Error writing to {file_path}: {str(e)}')