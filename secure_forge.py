import hashlib
import base64
from cryptography.fernet import Fernet

# --- CORE FUNCTIONS ---

def generate_hash(data):
    """
    Creates a SHA-256 digital fingerprint (integrity check).
    """
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest()

def encrypt_data(data, key):
    """
    Encrypts the data using AES-based Fernet symmetric encryption.
    """
    f = Fernet(key)
    return f.encrypt(data)

def decrypt_data(encrypted_data, key):
    """
    Decrypts the data back to its original form using the key.
    """
    f = Fernet(key)
    return f.decrypt(encrypted_data)

def encode_data(data):
    """
    Encodes binary data into a Base64 string for portability.
    """
    return base64.b64encode(data)

def decode_data(encoded_string):
    """
    Decodes a Base64 string back into binary format.
    """
    return base64.b64decode(encoded_string)

# --- MAIN EXECUTION PIPELINE ---

if __name__ == "__main__":
    # 1. INITIAL DATA
    original_message = b"This is a top-secret message for MIS students."
    print(f"[1] Original Message: {original_message.decode()}")

    # 2. GENERATE INTEGRITY SEAL (HASH)
    original_hash = generate_hash(original_message)
    print(f"[2] Original SHA-256 Hash: {original_hash}")

    # 3. ENCRYPTION (CONFIDENTIALITY)
    # Note: In a real app, save this key securely!
    secret_key = Fernet.generate_key() 
    encrypted_payload = encrypt_data(original_message, secret_key)
    print(f"[3] Encrypted Data (Raw Bytes): {encrypted_payload[:30]}...")

    # 4. ENCODING (PORTABILITY)
    final_output = encode_data(encrypted_payload)
    print(f"[4] Base64 Encoded Result: {final_output.decode()}")

    print("\n" + "="*50 + "\n")
    print("SIMULATING DATA TRANSMISSION...")
    print("\n" + "="*50 + "\n")

    # --- REVERSE PROCESS (THE RECEIVER) ---

    # 5. DECODING
    received_bytes = decode_data(final_output)

    # 6. DECRYPTION
    try:
        decrypted_result = decrypt_data(received_bytes, secret_key)
        print(f"[5] Decrypted Content: {decrypted_result.decode()}")

        # 7. FINAL INTEGRITY VERIFICATION
        received_hash = generate_hash(decrypted_result)
        print(f"[6] Received Hash: {received_hash}")

        if received_hash == original_hash:
            print("\n[SUCCESS] Verification Complete: Data is authentic and unmodified.")
        else:
            print("\n[ALERT] Integrity Breach: Data has been tampered with!")

    except Exception as e:
        print(f"[ERROR] Decryption failed. Incorrect key or corrupted data: {e}")