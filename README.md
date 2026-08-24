### Hexlet tests and linter status:
[![Actions Status](https://github.com/alexamuek/devops-engineer-from-scratch-project-313/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/alexamuek/devops-engineer-from-scratch-project-313/actions)  
To run web application run ```make run```  
The application will be available by url: localhost:8080.  
Use this url in your browser to interact to app

**Ways of app usage**  

*Dev mode*  
1. Run ```make run-local-postgres```  
2. Run ```make dev-concarently```  
The api will be available at http://127.0.0.1:8080/api/links  
The frontend will be available at http://localhost:5173/ which interracts to api

*Container mode*  
1. Run ```make build```  
2. Run ```make run-local-postgres```  
3. Run ```make run```  
The app will be available at http://127.0.0.1:8080/api/links

To run unit tests use ```make test```

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
- add env variables DATABASE_URL (internal url of run postgres in render), BASE_URL (render created url), SENTRY_DSN

