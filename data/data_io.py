import json

def load_json_data():
    """
    đọc dữ liệu
    """
    art_dict_data = list()
    with open("data/art_dict.json","r")as json_in:
        json_data = json.load(json_in)
    art_dict_data.extend(json_data)
    return art_dict_data

def write_json_data(json_data):
    """
    ghi dữ liệu
    """
    with open("data/art_dict.json","w")as json_out:
        json.dump(json_data, json_out, indent=4)

