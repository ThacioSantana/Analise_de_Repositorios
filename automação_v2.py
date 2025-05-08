# repositorio_analise.py
import argparse
import concurrent.futures
import json
import logging
import os
import re
import subprocess
import sys
import csv
from tqdm import tqdm

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("repositorio_analise.log"),
        logging.StreamHandler()
    ]
)

# --- Utilitários ---
class CloneError(Exception):
    def __init__(self, message):
        super().__init__(message)

def handle_error(error, context=""):
    if isinstance(error, CloneError):
        logging.error(f"Erro ao {context}: {error}")
    else:
        logging.exception(f"Erro inesperado ao {context}: {error}")

# --- Gera Relatório ---
def generate_report(directory, keywords, extensions):
    report_path = os.path.join(directory, 'relatorio.csv')
    found_lines = set()

    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            for i, line in enumerate(f):
                                for keyword in keywords:
                                    if re.search(rf"\b{re.escape(keyword)}\b", line):
                                        found_lines.add((file_path, i + 1, line.strip()))
                    except Exception as file_error:
                        logging.warning(f"Erro ao ler arquivo {file_path}: {file_error}")

        if found_lines:
            with open(report_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Arquivo', 'Linha', 'Conteúdo'])
                for item in sorted(found_lines):
                    writer.writerow(item)
            logging.info(f"Relatório CSV gerado com sucesso: {report_path}")
        else:
            logging.info("Nenhuma ocorrência encontrada para as palavras-chave.")

    except Exception as e:
        handle_error(e, context="gerar o relatório")

# --- Clona repositório ---
def fetch_repository(url, destination, keywords, extensions):
    try:
        repository_name = os.path.splitext(os.path.basename(url))[0]
        repository_dir = os.path.join(destination, repository_name)
        os.makedirs(repository_dir, exist_ok=True)

        subprocess.run([
            "git", "clone", url, repository_dir
        ], check=True, timeout=120, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        generate_report(repository_dir, keywords, extensions)

        return repository_name, True
    except Exception as e:
        handle_error(e, context=f"clonar o repositório '{url}'")
        return os.path.basename(url), False

# --- Carregador de URLs ---
def load_urls_from_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except Exception as e:
        handle_error(e, context="ler o arquivo de URLs")
        return []

# --- Função principal ---
def main(args=None):
    parser = argparse.ArgumentParser(
        description="Clona repositórios Git e gera relatórios CSV com palavras-chave encontradas.",
        epilog="Exemplo de uso: python repositorio_analise.py -d repositorios -f repos.txt"
    )
    parser.add_argument(
        "-d", "--directory", required=True,
        help="Diretório base onde os repositórios serão clonados."
    )
    parser.add_argument(
        "-u", "--urls", nargs='*',
        help="Lista de URLs de repositórios para clonar. Pode ser usada junto com -f."
    )
    parser.add_argument(
        "-f", "--url-file",
        help="Caminho para arquivo .txt contendo URLs de repositórios, uma por linha."
    )

    args = parser.parse_args(args)
    base_directory = args.directory
    urls = args.urls or []

    if args.url_file:
        urls.extend(load_urls_from_file(args.url_file))

    if not urls:
        raise CloneError("Nenhuma URL de repositório fornecida.")

    if not os.path.exists(base_directory):
        raise CloneError("O diretório base especificado não existe.")

    # Palavras-chave e extensões fixas no código (padrão)
    keywords = [
        'pwd', 'usr', 'username', 'password', 'usuario', 'senha',
        'UserSecret', 'Catalog', 'token'
    ]
    extensions = ['.json', '.xml', '.config', '.env']

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_repository, url, base_directory, keywords, extensions) for url in urls]

        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Processando repositórios"):
            repo_name, success = future.result()
            status = "sucesso" if success else "falha"
            logging.info(f"Clonagem e análise de {repo_name}: {status}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Uso: python repositorio_analise.py --help para instruções.")
        sys.exit(2)
    try:
        main()
    except Exception as e:
        handle_error(e, context="executar o programa principal")
