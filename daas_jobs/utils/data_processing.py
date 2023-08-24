import json
import time

def read_data():
    with open('output.json', 'r') as json_file:
        data = json.load(json_file)
        print("JSON data read from 'output.json'")
        return data
    
def write_data(new_data):
    data = read_data()
    data.update(new_data)
    with open('output.json', 'w') as json_file:
        json.dump(data, json_file)
    print("JSON data saved to 'output.json'")