import json, os
def save_json(file: str, data: dict):
    "removes old file and then replaces it with fresh data @tpowell11"
    os.remove(file)  # delete outdated data
    dumpData = json.dumps(data)
    with open(file, 'w') as f:  # open file
        f.write(dumpData)  # write the new json
        f.close()

def load_json(jsonfilename : str):
    with open(jsonfilename, 'r') as file:
        data = file.read()
        output = json.loads(data)
        file.close()
    return output