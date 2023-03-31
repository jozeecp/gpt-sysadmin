# GPT SysAdmin

gpt-sysadmin can SSH into host and autonomously execute intructions

## Linting

```bash
isort .
black .
pylint $(git ls-files '*.py') --rcfile=./.github/workflows/.pylintrc
```

## Unit Testing

```bash
python -m unittest discover tests
```
