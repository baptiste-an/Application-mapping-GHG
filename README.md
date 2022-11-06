# TSP Research Apps

## Requirements

### Pipenv

[Installation](https://pypi.org/project/pipenv/#installation)

```bash
pip install --user pipenv
pipenv --python 3.10 
pipenv install
pipenv shell
```

### Scalingo

Install Scalingo [cli](https://doc.scalingo.com/platform/cli/start)

```console
scalingo login
# add remote to the project
git remote add scalingo git@ssh.osc-fr1.scalingo.com:<app_name>.git
# deployment from mail
git push scalingo main
# deployment from another branch
git push scalingo <branch_name>:main

```
