import json


def add_listeners(i):
    i = str(i)
    with open('listen_users.json', 'r') as file:
        data = json.load(file)
    b = data.keys()
    if i not in b:
        data[i] = []

    print(data[i])
    print(type(data[i]))
    
  # Step 2: Modify the data structure
    #data['key1'] = 'new value2'  # Update an existing   key or add a new key-value pair
  # Step 3: Write the updated data structure back   to the JSON file
    with open('listen_users.json', 'w') as file:
        json.dump(data, file, indent=4)  # indent     parameter for pretty formatting (optional)

def update_listeners(i,cid, b: bool):
    """Updates the listener associated with i to include channel cid"""
    i = str(i)
    cid = str(cid)
    with open('listen_users.json', 'r') as file:
        data = json.load(file)
    b = data.keys()
    if i not in b:
        data[i] = [cid]
    else:
        data[i].append(cid)

    print(data[i])
    print(type(data[i]))
    
  # Step 2: Modify the data structure
    #data['key1'] = 'new value2'  # Update an existing   key or add a new key-value pair
  # Step 3: Write the updated data structure back   to the JSON file
    with open('listen_users.json', 'w') as file:
        json.dump(data, file, indent=4)  # indent     parameter for pretty formatting (optional)

def get_listeners(i):
    i = str(i)
    with open('listen_users.json', 'r') as file:
        data = json.load(file)
    if i in data.keys():
        return data[i]
    else:
        return []

def get_keys():
    with open('listen_users.json', 'r') as file:
        data = json.load(file)
    return data.keys()

def upd(i):
    i = str(i)
    with open('testingjson.json', 'r') as file:
        data = json.load(file)
    b = data.keys()
    print(b)
    print(i)
    print(i in b)

    if i in b:
        data[i].append(1)
    else:
        data[i] = []

    print(data[i])
    print(type(data[i]))
    
  # Step 2: Modify the data structure
    #data['key1'] = 'new value2'  # Update an existing   key or add a new key-value pair
  # Step 3: Write the updated data structure back   to the JSON file
    with open('testingjson.json', 'w') as file:
        json.dump(data, file, indent=4)  # indent     parameter for pretty formatting (optional)

def get_ssid(discord_id):
    i = str(discord_id)
    with open('users.json', 'r') as file:
        data = json.load(file)
    if i in data.keys():
        return data[i]
    else:
        return 0


#update_listeners(76561198991576823)