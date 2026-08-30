### Hexlet tests and linter status:
[![Actions Status](https://github.com/alexamuek/devops-engineer-from-scratch-project-313/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/alexamuek/devops-engineer-from-scratch-project-313/actions)  
This app is study project to get skills of deploy web app in production on PaaS. The app gives a possibility to create short links for user's urls, store it in DATABASE and have full circle of changing links. The backend is API developed via Flask and Python. The frontend was be gotten from school. It was be used Docker, reverse proxy via Nginx, Sentry, Postgres for deploying, development, catching of backend errors, store data.


**Ways of app usage**  

*Dev mode*  
1. Run ```make run-local-postgres```  
2. Run ```make dev-concarently```  
The api will be available at http://127.0.0.1:8080/api/links  
The frontend will be available at http://localhost:5173/ which interracts to api

*Container mode*  
1. Run ```make build```  
2. Run ```make run-local-postgres```  
3. Run ```make start-with-nginx```  
The app will be available at http://localhost:8080/#/links

To run unit tests use ```make test```
To run linter check use ```make lint```

It is nessesary to have .env.local for dev mode:  
```SENTRY_DSN=???  
LOCAL_POSTGRES_USER=myuser  
LOCAL_POSTGRES_PASSWORD=mypassword  
LOCAL_POSTGRES_DB=mydb  
LOCAL_POSTGRES_PORT=5432  
POSTGRES_CONTAINER_NAME=my-db  
DATABASE_URL=postgresql://myuser:mypassword@localhost:5432/mydb?sslmode=disable  
BASE_URL=http://127.0.0.1:8080/```  

For production deploy to render:  
- run postgres in render  
- add env variables DATABASE_URL (internal url of run postgres in render), BASE_URL (render created url), SENTRY_DSN, PORT (value 80)

