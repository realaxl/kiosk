import sqlite3
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent

# Manual URLs from https://binary-kitchen.github.io/SolderingTutorial/
# Mapping product names to their German PDF manual URLs
MANUAL_URLS = {
    "AxolotlBadge": "https://binary-kitchen.github.io/SolderingTutorial/kits/AxolotlBadge/manual_de.pdf",
    "BleepBot fully assembled": "https://binary-kitchen.github.io/SolderingTutorial/kits/BleepBot/manual_de.pdf",
    "Daisy RGB": "https://binary-kitchen.github.io/SolderingTutorial/kits/Daisy/manual_de.pdf",
    "Dino": "https://binary-kitchen.github.io/SolderingTutorial/kits/Dino/manual_de.pdf",
    "Heartbeat Herz Loetbausat07": "https://binary-kitchen.github.io/SolderingTutorial/kits/Heartbeat/manual_de.pdf",
    "MoonCat": "https://binary-kitchen.github.io/SolderingTutorial/kits/MoonCat/manual_de.pdf",
    "Motoerboerd bunter Vogelschwarm": "https://binary-kitchen.github.io/SolderingTutorial/kits/Motoerboerd/manual_de.pdf",
    "NibblePlusPlusSMD": "https://binary-kitchen.github.io/SolderingTutorial/kits/NibblePlusPlus/manual_de.pdf",
    "OwlThiefDIP": "https://binary-kitchen.github.io/SolderingTutorial/kits/OwlThief/manual_de.pdf",
    "RainbowButterfly": "https://binary-kitchen.github.io/SolderingTutorial/kits/RainbowButterfly/manual_de.pdf",
    "RainbowUnicorn01": "https://binary-kitchen.github.io/SolderingTutorial/kits/RainbowUnicorn/manual_de.pdf",
    "Regenbogen Rakete": "https://binary-kitchen.github.io/SolderingTutorial/kits/Rocket/manual_de.pdf",
    "RocketBadge": "https://binary-kitchen.github.io/SolderingTutorial/kits/RocketBadge/manual_de.pdf",
    "SawToothOrganDIP": "https://binary-kitchen.github.io/SolderingTutorial/kits/SawToothOrgan/manual_de.pdf",
}

def update_manual_urls():
    """Update manual URLs for products in the database"""
    db_path = PROJECT_ROOT / 'db' / 'db.sqlite'
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    updated_count = 0
    not_found_count = 0
    
    print("Updating manual URLs...\n")
    
    for product_name, manual_url in MANUAL_URLS.items():
        # Find product by name
        cursor.execute('SELECT productId, name, manualUrl FROM products WHERE name = ?', (product_name,))
        product = cursor.fetchone()
        
        if product:
            product_id, name, current_url = product
            
            # Update manual URL
            cursor.execute('UPDATE products SET manualUrl = ? WHERE productId = ?', (manual_url, product_id))
            print(f"[+] Updated: {name}")
            print(f"    URL: {manual_url}")
            updated_count += 1
        else:
            print(f"[!] Not found in DB: {product_name}")
            not_found_count += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Updated: {updated_count} products")
    print(f"  Not found: {not_found_count} products")
    print(f"{'='*60}")

if __name__ == '__main__':
    update_manual_urls()

# Made with Bob
