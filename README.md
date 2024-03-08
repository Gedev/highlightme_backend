# highlightme_backend
"python manage.py runserver" to run the python server

### Warcraft logs API uses GraphQL
The schema can be found here : https://fr.warcraftlogs.com/v2-api-docs/warcraft/

### Utiliser curl pour s'authentifier et recevoir le token d'authentification
curl -u "9b81c20f-c04a-46de-8063-f280d9f9b151:cXaiXGLTxqmc9UP1LitOOuyEXqOjmutKUd0wvt0K" -d grant_type=client_credentials https://www.warcraftlogs.com/oauth/token
{"token_type":"Bearer","expires_in":31104000,"access_token":"access token"}