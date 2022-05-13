<h1 align="center"> Analisador de Transações </h1>

## 📋SOBRE

A ideia desse projeto veio do Alura challenger e consiste em criar um siste que receba arquivos de transações do tipo CSV. Após o usuario importar esses arquivos o sistema automaticamente ira salvar cada transação em um banco de dados e realizar a análise de transações suspeitas 📒.

## 💻Tecnologias utilizadas

O projeto foi construido utilizando as seguintes tecnologias:

- Python
- Django
- HTML e CSS
- JavaScript
- Ajax

## Como baixar o projeto

```bash
    # Clonar o repositorio
    git clone https://github.com/Deyllon/alura_challenger.git

    #Entrar no diretório
    cd alura_challenger

    #Crie seu ambiente virtual

    #Instale as dependências 
    pip install -r requirements.txt

    #Crie o arquivo .env, no arquivo .env adicione os seguintes codigos

    SECRET_KEY = senha para a chave secreta
    EMAIL_HOST_USER = seu email
    EMAIL_HOST_PASSWORD = senha do email
    EMAIL_HOST = Hosto do email

    #Rode o server
    python manage.py runserver
```