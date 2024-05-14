[[_TOC_]]

| TTP ID |  |
|--|--|
| TTP Nome: | Script para automatizar a clonagem de repositórios Git e verificar automaticamente se eles contêm credenciais sensíveis nos arquivos |
| Plataformas | Linux, Windows, Mac |



# **Definição**
O código é um script em Python que automatiza o processo de clonagem de repositórios Git a partir de URLs fornecidas e gera relatórios baseados nos arquivos desses repositórios. Ele realiza as seguintes etapas:

**1 - Clonagem de Repositórios:**
- Recebe uma lista de URLs de repositórios Git e um diretório de destino.
- Para cada URL na lista, clona o repositório correspondente para o diretório de destino.

**2 - Geração de Relatórios:**
- Após a clonagem bem-sucedida de um repositório, analisa os arquivos do repositório em busca de credenciais sensíveis, como nomes de usuário e senhas.
- Gera um relatório listando os arquivos que contêm essas credenciais sensíveis.

**3 - Saída do Relatório:**
- Se nenhuma ocorrência de credenciais sensíveis for encontrada nos arquivos do repositório, o relatório não é gerado.
- Caso contrário, o relatório é escrito em um arquivo de texto no diretório do repositório.

**4 - Execução Principal:**
- Ao ser executado, o script solicita ao usuário o diretório base onde os repositórios serão clonados.
- Em seguida, clona os repositórios e gera os relatórios para análise posterior.

**5 - Limpeza de cache:**
- Após a clonagem de todos os repositórios, limpa as credenciais em cache do Git.

**6 - Tratamento de Erro:**
- O código lida com erros como diretório inexistente, erros de clonagem e erros inesperados, usando exceções personalizadas.

# **Referências**
**Python**: 
https://python-forum.io/
https://pypi.org/
https://docs.python.org/pt-br/3/library/os.html
https://docs.python.org/3/library/subprocess.html
https://docs.python.org/3/library/re.html

**Git**
https://git-scm.com/doc
https://git-scm.com/
