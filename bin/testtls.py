# testtls.py

__version__ = '1.0.0' # Major.Minor.Patch

import socket
import ssl

from sh import human
import os
import machine
import time



# Load your server certificate and key
# For this example, the certificate and key are stored as strings.
# In a real application, you might read these from files.
server_cert = """-----BEGIN CERTIFICATE-----
MIIDLTCCAhWgAwIBAgIUHVyMTVpxtZwOIeuoBzQ4dT0tn6AwDQYJKoZIhvcNAQEL
BQAwJjELMAkGA1UEBhMCVVMxCzAJBgNVBAgMAlRYMQowCAYDVQQKDAFlMB4XDTIz
MTEyMDEwNDUxM1oXDTQ5MDcxMTEwNDUxM1owJjELMAkGA1UEBhMCVVMxCzAJBgNV
BAgMAlRYMQowCAYDVQQKDAFlMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKC
AQEAzCNAYqrki+l0L8/HyWZIl+uQAcAc7/zEsG+SRbKIlc3Ztr93mTf0/8nVUrcJ
Swjd9xK8DaqjI3W1m/50lV7F9GN6IBXa5ohto38z31LTo6aEmjQcNnlRfam8cc/f
x/3ukHeKeMheXEasjmMqtuGy4NEnjBwxN4q8m8ArJ31O/bS7PqYnTB8OqGpI0I1w
Ly0A3MJO7mNHsRzV4VZvJiKTeev6oxcIjBJxg4RgSKz5Z1uXTiAmi+aSAcODbrqm
pmPqhS0zdIIKy98vyI2IHbn90c1Td5aPF/FAsIqtVP8qNQd4FW5TqFKA4aEsdn5E
Ghn60EFqtwYzeBrXeC497AQ5YwIDAQABo1MwUTAdBgNVHQ4EFgQU7iQ2XNug1qUq
aVAqV5O7qqv4GdAwHwYDVR0jBBgwFoAU7iQ2XNug1qUqaVAqV5O7qqv4GdAwDwYD
VR0TAQH/BAUwAwEB/zANBgkqhkiG9w0BAQsFAAOCAQEALBZKIGh2h+4sQ7osxmS5
jKeK267HYrQYSzHtkG9kift+H+wNI0Yf8Fly3OZrw8nWZmB/bdiSlorsbFlVDPXt
37oTa+7bD0VL9F7vDn29CYPVzgIW16l3mIPrxnXOEbjNctCD9vMogh3MxqOgzWqy
rtxWKKtrWNHvJAsk4eqvB6vt9Vj1Uuf6b64Z0ItNBtaiot/rVfZgTXJr04kb0Bxb
OXGqK8yhNu513StBiuLrGNGnT1Ta8IUBEyTK8riGeDskAm5dCB0ffIRqcl5fw8Qr
4SnmfvavxcH8JOs4QHlMTQdpi4TkbY+f+Mb42twXuepGRgL/m86kbk8ok8stL38f
fA==
-----END CERTIFICATE-----"""
server_key = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDMI0BiquSL6XQv
z8fJZkiX65ABwBzv/MSwb5JFsoiVzdm2v3eZN/T/ydVStwlLCN33ErwNqqMjdbWb
/nSVXsX0Y3ogFdrmiG2jfzPfUtOjpoSaNBw2eVF9qbxxz9/H/e6Qd4p4yF5cRqyO
Yyq24bLg0SeMHDE3irybwCsnfU79tLs+pidMHw6oakjQjXAvLQDcwk7uY0exHNXh
Vm8mIpN56/qjFwiMEnGDhGBIrPlnW5dOICaL5pIBw4NuuqamY+qFLTN0ggrL3y/I
jYgduf3RzVN3lo8X8UCwiq1U/yo1B3gVblOoUoDhoSx2fkQaGfrQQWq3BjN4Gtd4
Lj3sBDljAgMBAAECggEASgSiLOSQGBcfFNL/OwyGV+eHAMt68p2xZ9Qcsn7ovYC1
Z2kHYZwDjtfNLL/Hc9iUOykk3MO5gXsFzbk25o5FsrZ7KrUh+SMQtg7CbUBoEten
Dw7ECBB3Ntxbwty/5JEzdliR8fedF1Jc8QgODd/Kb3AHKetzAROiDcthGmF6Sc0f
q+Ay4UtN1K1rVZDmBF1iGz1kF5hJVO0LuMIYobRlQToL67qGejASpxaAq2CIsgft
46iLP/tlTny1Q49dstQuIpzyEwWAoOLzLEaW1isvVNyHrbrLKFSg1Zvjn2bE9Z+7
KggjlRNl91iAH8y9RNcOVvHEF6dxJD2UwyGvb6c4aQKBgQDlEeHF25sHKSK7hGy6
cwgltV0faoIcuQO0tl3u+dIiyBQ4c++FU37Pdy+tC4qTGWkuk1ASiXYFttL8MR25
lCoE8imiIEypGJG5YhFqisQGFgnBdfh1adxPST2YP9uaG+A2Frp245dfQ4xM7zXe
CDymstjgK7xZgLrZ4svt0U+1NQKBgQDkIwIUnJCUG3Qm+aAQCCS+RoChuy8v49+C
IJ6o9ka78BCQMFsqycJYvyEnWh9ZnlbmpkvXB0UQm81K1VK1LbLg5qewDdUunEN5
qYGsV1TtQDLUHiO4PIZ/+3dBoEIDsFh+L7+/zCSe3iTSrwlt8wzV9mMh+fGJQg6G
VDaJL+N/NwKBgFcqSMkrWYCODKNiLqV8JDuFGdxcgQpA9MINKw1GjsmhbOBWbWxE
a1qytbeZTq/O2ZFZiPykxf5CpWJFplP5p0uegm0o8ULfEISEZrAuAY13UVsGcvbq
w2SAMCoBEqU/uj+awnV/ARjE8VxNIihM5hdgstoKim9cZr2GaacjILuJAoGARCQs
v+lPyd01YVrYM1GrX+YBD82wN3ax0NVbbo447HO1DsxSvsIKuaVFCtMBYCxKOpRb
PLvgJijTNdHn5VPkBQb/+Tb4gPaNtO4rXEWtiTvOssrZ0nLJnbqHkWODtERc+jva
4zffjFA/4WoEwAGDyPjR/VkBiwTe/8Jxk6JpKhsCgYEA2ptnqtZq+uGgRpFnlrJd
2fRj50fVAq+mol1mVAVpYmlkTFLEbC7FLLHoMu2XkQax4teAyXgAtZ/kSogyK90D
d0NzfS8sPi0oKe57Ug5E9gsPBw+Q49MIvOBjPrOrG2vy/8Xbn2HR2vGYEUS3TuU6
FVYBVdicAne7/2GKhEoTovk=
-----END PRIVATE KEY-----"""

# Create a socket and wrap it in an SSL context
def create_ssl_socket(cert, key, port=443):
    addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]

    sock = socket.socket()
    sock.bind(addr)
    sock.listen(5)

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(cert, key)

    return sock, ssl_context

# Handle client connections
def serve_client(client_sock):
    client_stream = client_sock.makefile('rwb', 0)
    request = client_stream.readline()
    print('Request:', request)

    response = 'HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\nHello, world!'
    client_stream.write(response)
    client_stream.close()
    client_sock.close()

def main2():
    sock, ssl_context = create_ssl_socket(server_cert, server_key)

    while True:
        client_sock, addr = sock.accept()
        client_sock = ssl_context.wrap_socket(client_sock, server_side=True)
        print('Client connected from:', addr)

        try:
            serve_client(client_sock)
        except Exception as e:
            print('Client serving failed:', e)

#if __name__ == '__main__':
#    main()


def __main__(args):
    num = 10
    pin=2
    if len(args) > 2:
        pin = int(args[2])
    if len(args) > 3:
        num = int(args[3])
    ton = 1.0
    if len(args) > 4:
        ton = float(args[4])
    toff = 1.0
    if len(args) > 5:
        toff = float(args[5])
    
    if not num:
        num = 10

    #print("blink pin{} loop{} ondelay{} offdelay{}".format(pin, num, ton, toff))
    main2()
