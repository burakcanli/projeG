import json

def load_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Hata: {file_path} bulunamadı.")
        return None

def find_answer(data, user_input):
    if "is_plani" in data:
        for item in data["is_plani"]:
            if item["soru"].lower() in user_input.lower():
                return item["cevap"]
    
    if "pazar_arastirmasi" in data:
        for item in data["pazar_arastirmasi"]:
            if item["soru"].lower() in user_input.lower():
                return item["cevap"]
    
    if "finansman" in data:
        for item in data["finansman"]:
            if item["soru"].lower() in user_input.lower():
                return item["cevap"]
    
    return None
