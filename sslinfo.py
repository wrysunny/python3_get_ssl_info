import sys
import ssl
import socket
import OpenSSL.crypto as crypto

domain = sys.argv[1]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)
s.connect((domain, 443))
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
s = context.wrap_socket(s, server_hostname=domain)
cert = s.getpeercert(True)
x509 = crypto.load_certificate(crypto.FILETYPE_ASN1,cert)
print("Common Name: " + x509.get_subject().CN)

# if verity
#print "Organization: " + x509.get_subject().O
if x509.get_subject().O is None:
	print('Organization: None !')
else:
	print("Organization: " + x509.get_subject().O)

if x509.get_subject().OU is None:
	print('Organizational Unit: None !')
else:
	print("Organizational Unit: " + x509.get_subject().OU)

serial_number = '{0:x}'.format(int(x509.get_serial_number()))
if len(serial_number) % 2 != 0:
	serial_number = '0' + serial_number
b = []
l = len(serial_number)
for n in range(l):
	if n % 2 == 0:
		b.append(serial_number[n:n+2])
serial_number = ':'.join(b).upper()
print("Serial Number: " ,serial_number)
# get public key print(crypto.dump_publickey(crypto.FILETYPE_PEM,x509.get_pubkey()))
s.close()
