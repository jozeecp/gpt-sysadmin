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
