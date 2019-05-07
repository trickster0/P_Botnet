openssl genrsa -out ca.key 2048
openssl req -new -x509 -days 3500 -key ca.key -out ca.crt
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr
openssl x509 -req -days 3500 -in server.csr -CA ca.crt -CAkey ca.key -set_serial 01 -out server.crt
openssl pkcs12 -export -out server.p12 -inkey server.key -in server.crt -chain -CAfile ca.crt
rm server.p12 server.csr ca.key