import os
import re
import subprocess

def fetch_repository(url, destination):
    # Clone o repositório
    subprocess.run(["git", "clone", url, destination])

def search_and_extract_code(directory):
    # Verifica se o diretório existe
    if not os.path.isdir(directory):
        print("Diretório inválido!")
        return

    # Lista de extensões de arquivo para procurar
    extensions = ['.json', '.xml', '.config']

    # Lista de palavras-chave para procurar nas linhas dos arquivos
    keywords = ['pwd', 'usr', 'username', 'password', 'usuario', 'senha', 'UserSecret', 'Catalog']

    # Nome do relatório
    report_name = 'relatorio.txt'

    # Contador para evitar a sobrescrição do relatório
    count = 1

    # Loop através das extensões e palavras-chave
    for ext in extensions:
        for keyword in keywords:
            # Procura por arquivos com a extensão atual e extrai as linhas com as palavras-chave
            found_lines = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith(ext):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r') as f:
                            for line in f:
                                if re.search(keyword, line):
                                    found_lines.append(line)

            # Verifica se houve alguma linha encontrada
            if found_lines:
                # Salva o conteúdo no relatório com um nome único
                report_path = os.path.join(directory, f'{report_name}_{count}.txt')
                with open(report_path, 'w') as report_file:
                    report_file.writelines(found_lines)

                print(f"Relatório gerado com sucesso em {report_path}")
                count += 1

    if count == 1:
        print("Nenhuma linha encontrada nos arquivos.")

if __name__ == "__main__":
    # Solicita o URL do repositório
    repository_url = input("Digite a URL do repositório: ")
    # Solicita o diretório de destino
    destination_dir = input("Digite o diretório de destino para clonar o repositório: ")
    # Clona o repositório
    fetch_repository(repository_url, destination_dir)

    # Executa a busca e extração de código
    search_and_extract_code(destination_dir)
