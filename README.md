# 🔍 Análise de Repositórios Git

Este projeto contém um script Python para clonar repositórios Git, analisar arquivos em busca de credenciais sensíveis (como senhas e tokens), e gerar relatórios com os resultados.

---

## 🚀 Funcionalidades

- 📦 Clonagem de múltiplos repositórios (lista definida no código).
- 🔍 Busca por palavras-chave sensíveis como `senha`, `password`, `UserSecret`, entre outras.
- 🧠 Detecção automática de tokens **JWT** via regex.
- 📄 Geração de relatório `.txt` para cada repositório analisado.
- 📊 Geração de resumo em `.csv`, formatado corretamente para Excel.
- 🧹 Após a análise, remove os arquivos do repositório clonado, mantendo apenas o relatório.
- 📌 Tratamento de erros centralizado e log completo em `erros.log`.

---

## 🧑‍💻 Como usar

1. Abra o terminal.
2. Execute o script com Python:
   ```bash
   python analise_repositorios.py
   ```
3. Digite o caminho do diretório onde deseja clonar os repositórios.
4. O script irá clonar, analisar e gerar os relatórios automaticamente.

> ✅ A lista de repositórios está definida diretamente no código-fonte, dentro da variável `repository_urls`.

---

## 🔍 Palavras-chave e extensões analisadas

- **Palavras-chave buscadas:**
  ```
  pwd, usr, username, password, usuario, senha, UserSecret, Catalog
  ```

- **Extensões de arquivos analisadas:**
  ```
  .json, .xml, .config
  ```

- **Tokens JWT detectados** com regex:
  ```
  eyJ[a-zA-Z0-9_-]+.[a-zA-Z0-9_-]+.[a-zA-Z0-9_-]+
  ```

---

## 📁 Saída

- `relatorio.txt` → Gerado dentro de cada repositório, com linhas que contêm dados sensíveis.
- `relatorio_resumo.csv` → Resumo com contagem por repositório, compatível com Excel.
- `erros.log` → Registro de exceções e falhas encontradas.

## 📖 Referências

### Python
- https://docs.python.org/3/
- https://docs.python.org/3/library/os.html
- https://docs.python.org/3/library/subprocess.html
- https://docs.python.org/3/library/re.html
- https://docs.python.org/3/library/csv.html
- https://docs.python.org/3/library/shutil.html
- https://docs.python.org/3/library/logging.html
- https://docs.python.org/3/library/functools.html

### Git
- https://git-scm.com/doc
- https://git-scm.com/

---

## 📄 Estrutura Sugerida
```
/
├── repositorio_analise.py     # Versão atual (v2)
├── automacao_v1.py            # Versão anterior (v1)
├── repos.txt                  # Lista de URLs de repositórios
├── repositorio_analise.log    # Log da execução
└── /repositorios              # Diretório com repositórios clonados
