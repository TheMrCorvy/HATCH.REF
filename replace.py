import os
import re

files_to_update = [
    r"C:\Users\gonza\OneDrive\Desktop\localhost\HATCH_REF\Documentation\GameDesign\01-game-design-document.md",
    r"C:\Users\gonza\OneDrive\Desktop\localhost\HATCH_REF\Documentation\GameDesign\02-balance-curves-and-math.md",
    r"C:\Users\gonza\OneDrive\Desktop\localhost\HATCH_REF\Documentation\Furniture\01-furniture-catalog-and-store.md",
    r"C:\Users\gonza\OneDrive\Desktop\localhost\HATCH_REF\Documentation\Furniture\02-furniture-data-model.md",
    r"C:\Users\gonza\OneDrive\Desktop\localhost\HATCH_REF\Documentation\Furniture\03-furniture-placement-and-rendering.md"
]

def replace_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    
    replacements = [
        (r'\bPetGame\b', 'KaijuGame'),
        (r'\bpet_type\b', 'kaiju_type'),
        (r'\bpet_id\b', 'kaiju_id'),
        (r'\bPetStateNotifier\b', 'KaijuStateNotifier'),
        (r'\bPetState\b', 'KaijuState'),
        (r'\bpet room\b', 'containment room'),
        (r'\bpet sprite\b', 'kaiju sprite'),
        (r'\bpet store\b', 'kaiju store'),
        (r'\bpet inventory\b', 'kaiju inventory'),
        (r'\bpet name\b', 'kaiju designation'),
        (r'\bpet action\b', 'kaiju action'),
        (r'\bvirtual pet\b', 'virtual kaiju'),
        (r'\bdigital pet\b', 'digital kaiju'),
        (r'\bpet care\b', 'kaiju care'),
        (r'\bpet game\b', 'kaiju game'),
        (r'\bpetComponent\b', 'kaijuComponent'),
        (r'\bpet_sprite_sheet\b', 'kaiju_sprite_sheet'),
        (r'\bPetInstance\b', 'KaijuInstance'),
        
        (r'\bbunnies, cats, or dogs\b', 'godzillas, mothras, or rodans'),
        (r'\bbunny\b', 'godzilla'),
        (r'\bcat\b', 'godzilla'),
        (r'\bdog\b', 'godzilla'),
        (r'\bbird\b', 'godzilla'),
        (r'\bkitten\b', 'hatchling'),
        (r'\bpuppy\b', 'hatchling'),
        
        (r'\bpets\b', 'kaijus'),
        (r'\bPets\b', 'Kaijus'),
        (r'\bpet\b', 'kaiju'),
        (r'\bPet\b', 'Kaiju'),
        
        (r'\bspecies\b', 'kaiju type'),
        (r'\bSpecies\b', 'Kaiju Type'),
    ]

    for pattern, repl in replacements:
        content = re.sub(pattern, repl, content)

    # Special handling to prevent file path references from being broken
    # But since there are no pet-*.md files, we're mostly fine. Let's make sure it didn't mess up "pet" in any words. Word boundaries (\b) handles this.

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

for f in files_to_update:
    if os.path.exists(f):
        changed = replace_in_file(f)
        print(f"Changed {os.path.basename(f)}: {changed}")
    else:
        print(f"File not found: {f}")
