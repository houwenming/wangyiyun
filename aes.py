import base64
from Crypto.Cipher import AES

class AESCipher:

    def __init__(self, key):
        self.key = key[0:16] #只截取16位
        self.iv = "0102030405060708" # 16位字符，用来填充缺失内容，可固定值也可随机字符串，具体选择看需求。

    def __pad(self, text):
        """填充方式，加密内容必须为16字节的倍数，若不足则使用self.iv进行填充"""
        text_length = len(text)
        amount_to_pad = AES.block_size - (text_length % AES.block_size)
        if amount_to_pad == 0:
            amount_to_pad = AES.block_size
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad

    def __unpad(self, text):
        pad = ord(text[-1])
        return text[:-pad]

    def encrypt(self, raw):
        """加密"""
        raw = self.__pad(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(raw)) 

    def decrypt(self, enc):
        """解密"""
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv )
        return self.__unpad(cipher.decrypt(enc).decode("utf-8"))


if __name__ == '__main__':
    e = AESCipher('pSpVjRbPJVtitugH')
    secret_data = "XPuTsKOsBVKYtwzWmFGW3XUeHe7tifyZdKkFQa/wUuDb4SfMaf1qw76jWIJMKUIJ7pbifd+w7EXF7c1ha/MKQLFdNVpNeBIOCqXvmHpkshk="
    enc_str = e.encrypt(secret_data)
    print('enc_str: ' + enc_str.decode())
    dec_str = e.decrypt(enc_str)
    print('dec str: ' + dec_str)
