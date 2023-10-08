from cryptography.fernet import Fernet

# Generate a secret key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Read the contents of the .env file
with open('.env', 'rb') as file:
    file_contents = file.read()

# Encrypt the contents
encrypted_contents = cipher_suite.encrypt(file_contents)

# Save the encrypted contents to a file
with open('eenv', 'wb') as file:
    file.write(encrypted_contents)

# Save the encryption key to a file (keep this secret)
with open('ekey.key', 'wb') as key_file:
    key_file.write(key)
