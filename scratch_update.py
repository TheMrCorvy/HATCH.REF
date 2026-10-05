import os
import re

files = [
    r"C:\Users\gonza\OneDrive\Desktop\localhost\HATCH_REF\Documentation\Architecture\01-system-overview.md",
    r"C:\Users\gonza\OneDrive\Desktop\localhost\HATCH_REF\Documentation\Architecture\02-technology-stack-evaluation.md",
    r"C:\Users\gonza\OneDrive\Desktop\localhost\HATCH_REF\Documentation\Architecture\03-monorepo-structure.md",
    r"C:\Users\gonza\OneDrive\Desktop\localhost\HATCH_REF\Documentation\Architecture\04-backend-and-realtime.md",
    r"C:\Users\gonza\OneDrive\Desktop\localhost\HATCH_REF\Documentation\Architecture\05-database-and-auth.md",
    r"C:\Users\gonza\OneDrive\Desktop\localhost\HATCH_REF\Documentation\Architecture\06-offline-first-and-state.md",
]

def replace_terms(text):
    # Save file names to prevent changing them
    file_name_matches = re.findall(r'[\w\-]*pet[\w\-]*\.(?:dart|md)', text, flags=re.IGNORECASE)
    file_names = list(set(file_name_matches))
    placeholders = {f"__FILE_{i}__": name for i, name in enumerate(file_names)}
    for placeholder, name in placeholders.items():
        text = text.replace(name, placeholder)

    # Specific replacements based on instructions
    replacements = {
        r'\bvirtual pet\b': 'virtual kaiju',
        r'\bVirtual pet\b': 'Virtual kaiju',
        r'\bdigital pet\b': 'digital kaiju',
        r'\bDigital pet\b': 'Digital kaiju',
        r'\bpet care\b': 'kaiju care',
        r'\bPet care\b': 'Kaiju care',
        r'\bpet game\b': 'kaiju game',
        r'\bPet game\b': 'Kaiju game',
        r'\bpet room\b': 'containment room',
        r'\bPet room\b': 'Containment room',
        r'\bpet sprite\b': 'kaiju sprite',
        r'\bPet sprite\b': 'Kaiju sprite',
        r'\bpet store\b': 'kaiju store',
        r'\bPet store\b': 'Kaiju store',
        r'\bpet inventory\b': 'kaiju inventory',
        r'\bPet inventory\b': 'Kaiju inventory',
        r'\bpet inventories\b': 'kaiju inventories',
        r'\bpet name\b': 'kaiju designation',
        r'\bPet name\b': 'Kaiju designation',
        r'\bpet action\b': 'kaiju action',
        r'\bPet action\b': 'Kaiju action',
        r'\bPetStateNotifier\b': 'KaijuStateNotifier',
        r'\bPetNotifier\b': 'KaijuNotifier',
        r'\bPetState\b': 'KaijuState',
        r'\bPetGame\b': 'KaijuGame',
        r'\bpet_type\b': 'kaiju_type',
        r'\bpet_id\b': 'kaiju_id',
        r'\bpetComponent\b': 'kaijuComponent',
        r'\bpet_sprite_sheet\b': 'kaiju_sprite_sheet',
        r'\bspecies\b': 'kaiju type',
        r'\bSpecies\b': 'Kaiju type',
        r'\b(bunny|cat|dog|bird)\b': 'godzilla',
        r'\b(bunnies|cats|dogs|birds)\b': 'godzillas',
        r'\b(Bunny|Cat|Dog|Bird)\b': 'Godzilla',
        r'\b(Bunnies|Cats|Dogs|Birds)\b': 'Godzillas',
        r'\bkitten\b': 'hatchling',
        r'\bpuppy\b': 'hatchling',
        r'\bKitten\b': 'Hatchling',
        r'\bPuppy\b': 'Hatchling',
        r'\bPetInstance\b': 'KaijuInstance',
        r'\bactive_pet_sessions\b': 'active_kaiju_sessions',
        r'\bpet_catalog\b': 'kaiju_catalog',
        r'\bpet_lifecycle_config\b': 'kaiju_lifecycle_config',
    }

    for pattern, repl in replacements.items():
        text = re.sub(pattern, repl, text)

    def general_replacer(match):
        word = match.group(0)
        if word == 'pet': return 'kaiju'
        if word == 'Pet': return 'Kaiju'
        if word == 'PET': return 'KAIJU'
        if word == 'pets': return 'kaijus'
        if word == 'Pets': return 'Kaijus'
        if word == 'PETS': return 'KAIJUS'
        return word

    text = re.sub(r'\b(pet|pets|Pet|Pets|PET|PETS)\b', general_replacer, text)

    # Restore file names
    for placeholder, name in placeholders.items():
        text = text.replace(placeholder, name)

    return text

for file_path in files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        new_content = replace_terms(content)
        
        # Add humor note in system overview if not present
        if "01-system-overview.md" in file_path and "contrast is an explicit design choice" not in new_content:
            note = "\n\n> [!NOTE]\n> **Humor & Lore Note:** The contrast of a giant kaiju living in a normal containment room, going to school, and getting hungry like a regular tamagotchi is an explicit design choice. This absurdity is central to the game's charm."
            new_content = new_content + note
            
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {file_path}")
    except Exception as e:
        print(f"Error on {file_path}: {e}")
