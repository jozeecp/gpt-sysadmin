# GPT SysAdmin

gpt-sysadmin can SSH into host and autonomously execute intructions

## Deployment (Local)

```bash
export PUBLIC_KEY="$(cat ./test-key.pub)"
docker-compose build
docker-compose up
```

## Linting

```bash
isort .
black .
pylint $(git ls-files '*.py') --rcfile=./.github/workflows/.pylintrc
```

## Unit Testing (Disable for now)

```bash
python -m unittest discover tests
```

## Backend testing

### v1/tasks/ - POST

```bash
curl -X POST http://localhost:5000/v1/tasks \
     -H "Content-Type: application/json" \
     -d '{
           "engine": "gpt-3.5-turbo",
           "taskDescription": "Example task description",
           "host": "13e378c7-2ee6-4fef-bf1b-1893c97beb3e",
           "user": "root",
           "supervised": true,
           "engine": "gpt-3.5-turbo"
         }'
```

### v1/hosts/{host_id} - GET

```bash
curl -X GET "http://localhost/v1/hosts/{host_id}"
```

### v1/hosts/ - POST

```bash
curl -X POST http://localhost:5000/v1/hosts \
     -H "Content-Type: application/json" \
     -d '{
           "hostname": "example-host",
           "description": "Ubuntu running on docker container",
           "username": "root",
           "password": "PASSWORD"
         }'
```
