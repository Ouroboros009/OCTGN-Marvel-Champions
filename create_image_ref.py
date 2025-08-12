import json
import os

output_file = "database_images.json"
packs_file = r"C:\github\marvelsdb_fanmade_data\packs.json"
packs_fanmade_file = r"C:\github\marvelsdb_fanmade_data\packs_fanmade.json"
input_dir = r"C:\github\marvelsdb_fanmade_data\pack"

# Charge les données des packs officiels
with open(packs_file, encoding="utf-8") as pf:
    packs_data = json.load(pf)

# Charge les données des packs fanmade
with open(packs_fanmade_file, encoding="utf-8") as pfm:
    packs_fanmade_data = json.load(pfm)

# Fusionne les deux listes de packs
all_packs_data = packs_data + packs_fanmade_data
packs_dict = {pack["code"]: pack for pack in all_packs_data}

cards = []
for filename in os.listdir(input_dir):
    if filename.endswith(".json"):
        filepath = os.path.join(input_dir, filename)
        with open(filepath, encoding="utf-8") as infile:
            try:
                data = json.load(infile)
                for card in data:
                    pack_code = card.get("pack_code", "")
                    pack_octgn_id = packs_dict.get(pack_code, {}).get("octgn_id", "")
                    filtered_card = {
                        "pack_code": pack_code,
                        "card_id": card.get("code", ""),
                        "name": card.get("name", ""),
                        "type": card.get("type_code", ""),
                        "octgn_id": card.get("octgn_id", ""),
                        "pack_octgn_id": pack_octgn_id
                    }
                    cards.append(filtered_card)
            except Exception as e:
                print(f"Erreur dans {filename} : {e}")

print("Nombre de cartes :", len(cards))  # TRACE

with open(output_file, "w", encoding="utf-8") as outfile:
    json.dump(cards, outfile, ensure_ascii=False, indent=2)