import base64
import os
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from getpass import getpass
import time

# --- CONFIGURATION (AYARLAR) ---
VAULT_FILE = "vault.json.enc"
# In a real app, salt should be random and stored per user. 
# For this MVP, we use a static salt to keep it simple.
SALT = b'my_static_secret_salt_v1' 

# --- CRYPTOGRAPHY ENGINE (ŞİFRELEME MOTORU) ---
def generate_key(master_password: str):
    """
    Derives a strong encryption key from the user's password using PBKDF2.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=100000,
    )   
    # Fernet requires a base64 encoded key
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

def encrypt_vault(key, data_dict: dict):
    """Encrypts the Python dictionary into bytes."""
    json_string = json.dumps(data_dict)
    return Fernet(key).encrypt(json_string.encode())

def decrypt_vault(key, encrypted_data: bytes):
    """Decrypts bytes back into a Python dictionary."""
    try:
        f = Fernet(key)
        decrypted_data = f.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode())
    except Exception:
        return None # Decryption failed (Wrong password)

# --- FILE OPERATIONS (DOSYA İŞLEMLERİ) ---
def initialize_vault(key):
    """Creates a new empty vault file if it doesn't exist."""
    if not os.path.exists(VAULT_FILE):
        empty_data = {"items": []}
        encrypted = encrypt_vault(key, empty_data)
        with open(VAULT_FILE, "wb") as f:
            f.write(encrypted)
        print(f"[System] New vault created: {VAULT_FILE}")

def save_vault(key, current_data: dict):
    """Saves the current state of data to the disk securely."""
    encrypted = encrypt_vault(key, current_data)
    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted)
    print("[System] Changes saved to disk.")

# --- FEATURES (ÖZELLİKLER) ---
def add_entry(current_data: dict):
    print("\n--- ADD NEW PASSWORD ---")
    website = input("Website/App Name: ")
    username = input("Username: ")
    password = input("Password: ")
    
    new_item = {
        "website": website,
        "username": username,
        "password": password
    }
    current_data["items"].append(new_item)
    print(f"[Success] Saved entry for {website}")
    return current_data

def list_entries(current_data: dict):
    print("\n--- YOUR PASSWORDS ---")
    if not current_data["items"]:
        print("Vault is empty.")
        return

    for item in current_data["items"]:
        print(f"- {item['website']} (User: {item['username']})")

def search_entry(current_data: dict):
    print("\n--- SEARCH ---")
    query = input("Search for website: ").lower()
    found = False
    
    for item in current_data["items"]:
        if query in item["website"].lower():
            print(f"\nFOUND: {item['website']}")
            print(f"Username: {item['username']}")
            print(f"Password: {item['password']}")
            print("-" * 20)
            found = True
            
    if not found:
        print("No matches found.")

def delete_entry(current_data: dict):
    print("\n--- DELETE ---")
    target = input("Exact website name to delete: ")
    
    # We create a new list excluding the item we want to delete
    new_items = []
    found = False
    
    for item in current_data["items"]:
        if item["website"] == target:
            found = True # Do not add to new list (effectively deleting it)
        else:
            new_items.append(item)
            
    if found:
        current_data["items"] = new_items
        print(f"[Success] {target} has been deleted.")
    else:
        print("[Error] Website not found.")
        
    return current_data

# --- MAIN LOOP (ANA DÖNGÜ) ---
def main_menu():
    print("\n" + "="*25)
    print(" 1. Add Entry")
    print(" 2. List Entries")
    print(" 3. Search Entry")
    print(" 4. Delete Entry")
    print(" 5. Exit")
    print("="*25)
    return input("Select Option: ")

if __name__ == "__main__":
    # 1. Login Step
    master_pw = getpass("Enter Master Password: ")
    key = generate_key(master_pw)
    
    # 2. Setup Step
    initialize_vault(key)
    
    # 3. Load & Decrypt Step
    with open(VAULT_FILE, "rb") as f:
        file_content = f.read()
        
    vault_data = decrypt_vault(key, file_content)
    
    if vault_data is None:
        print("\n[CRITICAL ERROR] Wrong password or corrupted file!")
    else:
        print(f"\n[WELCOME] Vault unlocked. {len(vault_data['items'])} entries loaded.")
        
        while True:
            choice = main_menu()
            
            if choice == "1":
                vault_data = add_entry(vault_data)
                save_vault(key, vault_data) # Auto-save
            elif choice == "2":
                list_entries(vault_data)
            elif choice == "3":
                search_entry(vault_data)
            elif choice == "4":
                vault_data = delete_entry(vault_data)
                save_vault(key, vault_data) # Auto-save
            elif choice == "5":
                print("Locking vault... Goodbye!")
                break
            else:
                print("Invalid option.")
                
time.sleep(5)
os.system('cls')
