import secrets

# Clé secrète robuste générée avec "secrets.token_urlsafe(50)" de DJANGO. 
# Une clé aléatoire robuste, adaptée à SECRET_KEY.
# Qui sera mise ensuite dans le fichier .env
print(secrets.token_urlsafe(50))

