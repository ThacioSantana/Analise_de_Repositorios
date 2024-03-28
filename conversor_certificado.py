from cryptography import x509
from cryptography.hazmat.backends import default_backend
import subprocess
import os

def validate_certificate(cert_path):
    try:
        with open(cert_path, 'rb') as cert_file:
            cert_data = cert_file.read()
            cert = x509.load_pem_x509_certificate(cert_data, default_backend())
            print("O certificado é válido e não está corrompido.")
    except Exception as e:
        print(f"Erro ao validar o certificado: {e}")

def convert_cert_to_pem(cert_path, output_path):
    try:
        if os.path.exists(output_path):
            print("O certificado já foi convertido para PEM.")
            return

        with open(cert_path, 'rb') as cert_file:
            cert_data = cert_file.read()
            cert = x509.load_der_x509_certificate(cert_data, default_backend())

            with open(output_path, 'wb') as pem_file:
                pem_file.write(cert.public_bytes(encoding=x509.Encoding.PEM))

        print(f"Certificado convertido para {output_path} com sucesso!")
    except Exception as e:
        print(f"Erro ao converter certificado: {e}")

def load_certificate_with_openssl(cert_path):
    try:
        # Comando OpenSSL para carregar o certificado
        command = f'openssl x509 -in {cert_path} -text -noout'
        
        # Executar o comando e capturar a saída
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, encoding='utf-8')
        
        # Imprimir a saída
        print(output)
        
        print("Certificado carregado com sucesso usando OpenSSL!")
    except subprocess.CalledProcessError as e:
        # Se ocorrer um erro ao chamar o processo
        print(f"Erro ao carregar o certificado com OpenSSL: {e}")

def main():
    cert_path = r'C:\Users\4063856\Documents\Programação\repositorios.banese.com.br.crt'
    pem_output_path = r'C:\Users\4063856\Documents\Programação\repositorios.banese.com.br.pem'
    
    validate_certificate(cert_path)
    convert_cert_to_pem(cert_path, pem_output_path)
    load_certificate_with_openssl(cert_path)

if __name__ == "__main__":
    main()
