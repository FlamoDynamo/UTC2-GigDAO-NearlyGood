from Crypto.Cipher import AES
import base64
import os

class CryptoUtils:
    def __init__(self, aes_key):
        # Giải mã khóa AES từ base64
        self.aes_key = base64.b64decode(aes_key)

    @staticmethod
    def generate_aes_key():
        """Generate a random AES key."""
        return base64.b64encode(os.urandom(32)).decode('utf-8')  # 32 bytes = 256 bits

    def encrypt(self, plaintext):
        # Tạo nonce (khóa ngẫu nhiên)
        nonce = os.urandom(16)
        cipher = AES.new(self.aes_key, AES.MODE_EAX, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())
        # Kết hợp nonce, tag và ciphertext
        return base64.b64encode(nonce + tag + ciphertext).decode('utf-8')

    def decrypt(self, enc_data):
        # Giải mã dữ liệu đã mã hóa
        try:
            enc_data_bytes = base64.b64decode(enc_data)
            nonce, tag, ciphertext = enc_data_bytes[:16], enc_data_bytes[16:32], enc_data_bytes[32:]
            cipher = AES.new(self.aes_key, AES.MODE_EAX, nonce=nonce)
            return cipher.decrypt_and_verify(ciphertext, tag).decode()
        except ValueError:
            print("Decryption failed: Invalid data.")
            return None

    def encrypt_bytes(self, data_bytes):
        """Encrypt binary data."""
        nonce = os.urandom(16)
        cipher = AES.new(self.aes_key, AES.MODE_EAX, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(data_bytes)
        return base64.b64encode(nonce + tag + ciphertext).decode('utf-8')

    def decrypt_bytes(self, enc_data_bytes):
        """Decrypt binary data."""
        try:
            enc_data = base64.b64decode(enc_data_bytes)
            nonce, tag, ciphertext = enc_data[:16], enc_data[16:32], enc_data[32:]
            cipher = AES.new(self.aes_key, AES.MODE_EAX, nonce=nonce)
            return cipher.decrypt_and_verify(ciphertext, tag)
        except ValueError:
            print("Decryption failed: Invalid data.")
            return None

# Ví dụ sử dụng
AES_KEY = 'GByT3lmFRnLg68bm6oq5is6v4j42kxyniHJRg+sqw40='
crypto_utils = CryptoUtils(AES_KEY)

# Mã hóa user_id
user_id = "123456"
encrypted_user_id = crypto_utils.encrypt(user_id)

# Giải mã
decrypted_user_id = crypto_utils.decrypt(encrypted_user_id)

print(f"Encrypted User ID: {encrypted_user_id}")
print(f"Decrypted User ID: {decrypted_user_id}")

# Sinh khóa AES mới
new_aes_key = crypto_utils.generate_aes_key()
print(f"Generated AES Key: {new_aes_key}")