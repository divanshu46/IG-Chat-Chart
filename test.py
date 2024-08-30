import json

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Example usage
file_path = r"C:\Users\MP-MOH-LAP-D121\test\ig_chat_ chart\instagram_data_analysis\data\message_1.json"
data = load_json(file_path)

# Print the structure of the JSON data
print(json.dumps(data, indent=4))