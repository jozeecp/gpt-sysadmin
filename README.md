# GPT SysAdmin

gpt-sysadmin can SSH into host and autonomously execute intructions

## Deployment (Local)

```bash
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
           "hostDescription": "Example host description",
           "host": "example.com",
           "user": "example_user",
           "supervised": true,
           "engine": "gpt-3.5-turbo"
         }'
```

### v1/hosts/ - POST

```bash
curl -X POST http://localhost:5000/v1/hosts \
     -H "Content-Type: application/json" \
     -d '{
           "host_name": "example-host",
           "ip": "192.168.1.100",
           "username": "example_user",
           "private_key": "example-private-key",
           "public_key": "example-public-key"
         }'
```
