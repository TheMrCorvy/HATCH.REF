import os
import re

files = [
    r"C:\Users\gonza\OneDrive\Desktop\localhost\HATCH_REF\Documentation\Plugins\01-plugin-architecture-overview.md",
    r"C:\Users\gonza\OneDrive\Desktop\localhost\HATCH_REF\Documentation\Plugins\02-user-triggered-actions.md",
    r"C:\Users\gonza\OneDrive\Desktop\localhost\HATCH_REF\Documentation\Plugins\03-non-user-triggered-actions.md",
    r"C:\Users\gonza\OneDrive\Desktop\localhost\HATCH_REF\Documentation\Plugins\04-scenarios-and-environments.md",
    r"C:\Users\gonza\OneDrive\Desktop\localhost\HATCH_REF\Documentation\Plugins\05-backend-control-and-schemas.md",
    r"C:\Users\gonza\OneDrive\Desktop\localhost\HATCH_REF\Documentation\Plugins\Minigames\01-minigame-overview.md",
    r"C:\Users\gonza\OneDrive\Desktop\localhost\HATCH_REF\Documentation\Plugins\Minigames\02-session-lifecycle-and-categories.md",
    r"C:\Users\gonza\OneDrive\Desktop\localhost\HATCH_REF\Documentation\Plugins\Minigames\03-backend-schema-and-rewards.md"
]

replacements = [
    (re.compile(r'\bpet_id\b'), 'kaiju_id'),
    (re.compile(r'\bpet_type\b'), 'kaiju_type'),
    (re.compile(r'\bpetComponent\b'), 'kaijuComponent'),
    (re.compile(r'\bpet_sprite_sheet\b'), 'kaiju_sprite_sheet'),
    (re.compile(r'\bPetGame\b'), 'KaijuGame'),
    (re.compile(r'\bPetStateNotifier\b'), 'KaijuStateNotifier'),
    (re.compile(r'\bPetState\b'), 'KaijuState'),
    
    (re.compile(r'\bpet room\b', re.IGNORECASE), 'containment room'),
    (re.compile(r'\bpet sprite\b', re.IGNORECASE), 'kaiju sprite'),
    (re.compile(r'\bpet store\b', re.IGNORECASE), 'kaiju store'),
    (re.compile(r'\bpet inventory\b', re.IGNORECASE), 'kaiju inventory'),
    (re.compile(r'\bpet name\b', re.IGNORECASE), 'kaiju designation'),
    (re.compile(r'\bpet action\b', re.IGNORECASE), 'kaiju action'),
    (re.compile(r'\bvirtual pet\b', re.IGNORECASE), 'virtual kaiju'),
    (re.compile(r'\bdigital pet\b', re.IGNORECASE), 'digital kaiju'),
    (re.compile(r'\bpet care\b', re.IGNORECASE), 'kaiju care'),
    (re.compile(r'\bpet game\b', re.IGNORECASE), 'kaiju game'),
    
    (re.compile(r'\bspecies\b', re.IGNORECASE), lambda m: 'Kaiju type' if m.group(0)[0].isupper() else 'kaiju type'),
    (re.compile(r'\bbunny\b|\bcat\b|\bdog\b|\bbird\b', re.IGNORECASE), lambda m: 'Godzilla' if m.group(0)[0].isupper() else 'godzilla'),
    (re.compile(r'\bkitten\b|\bpuppy\b', re.IGNORECASE), lambda m: 'Hatchling' if m.group(0)[0].isupper() else 'hatchling'),

    (re.compile(r'\bpet\b'), 'kaiju'),
    (re.compile(r'\bPet\b'), 'Kaiju'),
    (re.compile(r'\bPET\b'), 'KAIJU'),
    (re.compile(r'\bpets\b'), 'kaijus'),
    (re.compile(r'\bPets\b'), 'Kaijus'),
    (re.compile(r'\bPETS\b'), 'KAIJUS'),
]

for filepath in files:
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original_content = content
    for pattern, repl in replacements:
        content = pattern.sub(repl, content)
        
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filepath}")
    else:
        print(f"No changes: {filepath}")

print("Done")
