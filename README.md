# Repositório: Análise de Repositórios Git

Este projeto contém duas versões de um script Python que automatiza a clonagem de repositórios Git e a análise de arquivos em busca de credenciais sensíveis. Os resultados são gerados em relatórios CSV.

---

## 📊 Versão 2: `repositorio_analise.py` (Atual)

### 🔄 Funcionalidades:
1. **Clonagem paralela** de vários repositórios a partir de uma lista de URLs.
2. **Análise de arquivos** por palavras-chave sensíveis: `senha`, `password`, `token`, etc.
3. **Relatório CSV** gerado para cada repositório com as ocorrências encontradas.
4. **Barra de progresso** visual usando `tqdm`.
5. **Suporte a entradas por argumentos:**
   - URLs diretas via `-u`
   - Arquivo `.txt` com URLs via `-f`
   - Diretório de destino via `-d`
6. **Registro de logs** estruturados em `repositorio_analise.log`

### 🔧 Exemplo de uso:
```bash
python repositorio_analise.py -d ./repositorios -f repos.txt
```

### 🔍 Palavras-chave e extensões analisadas:
- **Palavras-chave:** `pwd`, `usr`, `username`, `password`, `usuario`, `senha`, `UserSecret`, `Catalog`, `token`
- **Extensões de arquivo:** `.json`, `.xml`, `.config`, `.env`

### 🔒 Exemplo de relatório:
```
Arquivo, Linha, Conteúdo
config.json, 12, "password": "admin123"
.env, 3, TOKEN=abcdef12345
```

---

## 🔄 Versão 1: `automacao_v1.py` (Antiga)

### 🔧 Funcionalidades:
1. Clonagem sequencial de repositórios.
2. Gera relatórios em arquivo `.txt` com as ocorrências.
3. Palavras-chave e extensões codificadas no script.
4. Solicita diretório via `input()`.
5. Limpa cache de credenciais Git após execução.
6. Usa exceções personalizadas para tratamento de erro.

---

## 📖 Referências

### Python
- https://docs.python.org/3/
- https://pypi.org/project/tqdm/
- https://docs.python.org/3/library/argparse.html
- https://docs.python.org/3/library/os.html
- https://docs.python.org/3/library/subprocess.html
- https://docs.python.org/3/library/re.html
- https://docs.python.org/3/library/concurrent.futures.html
- https://docs.python.org/3/library/logging.html
- https://docs.python.org/3/library/csv.html

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
