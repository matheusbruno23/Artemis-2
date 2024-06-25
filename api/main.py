import json
import re
import pandas as pd
import time
import jmespath
import os
from typing import Dict
import random
import MySQLdb
import httpx as x
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

#CONEXÃO DB

connection = MySQLdb.connect(
  host=os.getenv("DATABASE_HOST"),
  user=os.getenv("DATABASE_USERNAME"),
  passwd=os.getenv("DATABASE_PASSWORD"),
  db=os.getenv("DATABASE"),
  autocommit=True,
  ssl_mode="VERIFY_IDENTITY",
  ssl={ "ca": "/etc/ssl/certs/ca-certificates.crt" }
)

# Create a cursor to interact with the database
cursor = connection.cursor()
    
# CRIAÇÃO DE CLIENT PARA BUSCAR DE API COM IP REMOTO
   
client = x.Client(
    headers={
        # this is internal ID of an instegram backend app. It doesn't change often.
        "x-ig-app-id": "936619743392459",
        # use browser-like features
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "*/*",
    }
)

# BUSCA NA API PELO NOME DE USUÁRIO E RETORNA TODOS OS DADOS EM JSON
def scrape_user(username: str):
    a = random.uniform(0, 1)
    delay = (a * 2) + 4
    time.sleep(delay)
    result = client.get(f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",)
    data = json.loads(result.content)
    return data["data"]["user"]["biography"]


# ATIVAÇÃO DO ARQUIVO
def main():
    cursor.execute("SELECT * FROM followersAndBios WHERE bio LIKE '';")
    users = cursor.fetchall()
    for user in users:
        username = user[1]
        bio = scrape_user(username)
        if not bio:
            bio = "NOT_DEFINED"
        print(bio, username)
        cursor.execute(f"UPDATE followersAndBios SET bio = '{bio}' WHERE username = '{username}';")
    return 

# CONFIGURAÇÃO DO ARQUIVO

handler = main

if __name__ == "__main__":
    main()


    