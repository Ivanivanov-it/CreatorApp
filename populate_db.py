import os
import django
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CreatorApp.settings')
django.setup()

from characters.models import Character
from enemies.models import Enemy
from partners.models import Partner
from common.models import Role
from common.choices import CharacterType

def populate():
    # 1. Ensure Roles exist
    roles = []
    for role_choice in Role.RoleType.choices:
        role, _ = Role.objects.get_or_create(role=role_choice[0])
        roles.append(role)

    character_types = [choice[0] for choice in CharacterType.choices]

    # Helper to generate valid stats
    def generate_stats(max_total):
        # Ensure at least 1 for each and sum <= max_total
        total = random.randint(10, max_total)
        atk = random.randint(1, total - 2)
        dfs = random.randint(1, total - atk - 1)
        hp = total - atk - dfs
        return atk, dfs, hp

    # 2. Create 10 Characters
    print("Creating Characters...")
    characters = []
    for i in range(1, 11):
        name = f"Hero {i}"
        title = f"Champion of {i}"
        atk, dfs, hp = generate_stats(100)
        
        char, created = Character.objects.get_or_create(
            name=name,
            defaults={
                'title': title,
                'type': random.choice(character_types),
                'description': f"Description for {name}, known as {title}.",
                'attack': atk,
                'defense': dfs,
                'hp': hp,
            }
        )
        if created:
            # Add random roles
            char.roles.set(random.sample(roles, random.randint(1, 3)))
            print(f"Created {char.name}")
        else:
            print(f"Character {name} already exists.")
        characters.append(char)

    # 3. Create 10 Enemies
    print("\nCreating Enemies...")
    for i in range(1, 11):
        name = f"Villain {i}"
        title = f"Scourge of {i}"
        atk, dfs, hp = generate_stats(250)
        
        enemy, created = Enemy.objects.get_or_create(
            name=name,
            defaults={
                'title': title,
                'type': random.choice(character_types),
                'description': f"Description for {name}, known as {title}.",
                'attack': atk,
                'defense': dfs,
                'hp': hp,
            }
        )
        if created:
            # Add random weaknesses
            enemy.weakness.set(random.sample(roles, random.randint(1, 3)))
            print(f"Created {enemy.name}")
        else:
            print(f"Enemy {name} already exists.")

    # 4. Create 2 Partners for each Character (20 total)
    print("\nCreating Partners...")
    for char in characters:
        for p_idx in range(1, 3):
            name = f"Partner {p_idx} of {char.name}"
            title = f"Ally to {char.name} {p_idx}"
            atk, dfs, hp = generate_stats(40)
            
            partner, created = Partner.objects.get_or_create(
                name=name,
                defaults={
                    'title': title,
                    'description': f"A dedicated partner to {char.name}.",
                    'attack': atk,
                    'defense': dfs,
                    'hp': hp,
                    'character': char
                }
            )
            if created:
                partner.roles.set(random.sample(roles, random.randint(1, 2)))
                print(f"Created Partner {partner.name} for {char.name}")
            else:
                print(f"Partner {name} already exists.")

    print("\nPopulation complete!")

if __name__ == '__main__':
    populate()
