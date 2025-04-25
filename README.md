# YouTube Users from Channel 🧠📺

Este projeto em Python utiliza a [YouTube Data API v3](https://developers.google.com/youtube/v3) para listar usuários que comentaram nos vídeos mais recentes de um canal.

---

## 🔧 Como rodar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/youtube-users-from-channel.git
cd youtube-users-from-channel

```

### 2. Crie um ambiente virtual (recomendado)

```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Configure sua chave da Youtube API

Abra o arquivo src/main.py e substitua o valor da variável API_KEY pela sua chave válida:

```bash
API_KEY = "SUA_CHAVE_AQUI"
```

Você pode obter sua chave em Google Developers Console.

### 6. Execute o script

```bash
python src/main.py "Nome do Canal"
```

Exemplo:

```bash
python src/main.py "Canal Nostalgia"
```

### ✅ Como rodar os testes unitários

Certifique-se de que o ambiente virtual esteja ativado.
Execute:

```bash
pytest
```

Isso irá rodar todos os testes localizados no diretório 'tests/'.
