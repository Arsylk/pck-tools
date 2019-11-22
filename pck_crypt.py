from Crypto.Cipher import AES

key = b"\x37\xea\x79\x85\x86\x29\xec\x94\x85\x20\x7c\x1a\x62\xc3\x72\x4f\x72\x75\x25\x0b\x99\x99\xbd\x7f\x0b\x24\x9a\x8d\x85\x38\x0e\x39"
decipher = AES.new(key, AES.MODE_ECB)

def decrypt(file_bytes):
    padding = (16 - (len(file_bytes) % 16))
    file_bytes += padding * b"\x00"
    return decipher.decrypt(file_bytes)[:len(file_bytes)-padding]
	
	
#byte[] key = new byte[]
#            {
#                0xEF, 0xBB, 0xBF, 0xEC, 0x8B, 0x9C, 0xED, 0x94,
#                0x84, 0xED, 0x8A, 0xB8, 0xEC, 0x97, 0x85, 0xEA,
#                0xB3, 0xBC, 0xEB, 0x9D, 0xBC, 0xEC, 0x9D, 0xB8,
#                0xEA, 0xB2, 0x8C, 0xEC, 0x9E, 0x84, 0xEC, 0xA6
#            };