import git
import time

def clone_repository(repo_url, clone_path):
    git.Repo.clone_from(repo_url, clone_path)

def read_repository_data(repo_path):
    with open(repo_path, 'r') as file:
        data = file.read()
    return data

def store_data_to_txt(data, output_file):
    with open(output_file, 'w') as file:
        file.write(data)

def main(repo_url, clone_path):
    clone_repository(repo_url, clone_path)
    data = read_repository_data(clone_path)
    timestamp = int(time.time()) # Obter o timestamp atual
    output_file = f"data_{timestamp}.txt" # Nome do arquivo com timestamp
    store_data_to_txt(data, output_file)

if __name__ == "__main__":
    repo_url = input("Informe a URL do repositório: ")
    clone_path = input("Informe o caminho para clonar o repositório: ")
    main(repo_url, clone_path)
