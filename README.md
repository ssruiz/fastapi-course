# Complaint system

Complaints system using FastAPI

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip install -r requirements.txt
```

Create a .env file with the variables shown in [.env.template](.env.template)

## Usage

### DB

```bash
docker-compose up -d
```

Create a db with the DB_NAME enviroment variable value

(Some default values are included in [.env.template](.env.template) )

### App

```bash
uvicorn main:app --reload
```

### Swagger

```
http://127.0.0.1:8000/docs
```

## Built with

* [![FastAPI][FastAPI]][FastAPI-url]
* [![Docker][Docker]][Docker-url]
* [![POSTGRESQL][POSTGRESQL]][POSTGRESQL-url]
* [![AWSS3][AWSS3]][AWSS3-url]
* [![AWSSeS][AWSSES]][AWSSES-url]

* [![WISE][WISE]][WISE-url]

## License

[MIT](https://choosealicense.com/licenses/mit/)


[FastAPI]: https://img.shields.io/badge/FastApi-009688?style=for-the-badge&logo=fastapi&logoColor=white

[FastAPI-url]: https://fastapi.tiangolo.com/

[Docker]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white

[Docker-url]: https://www.docker.com/

[AWSS3]: https://img.shields.io/badge/Aws%20S3-569A31?style=for-the-badge&logo=amazons3&logoColor=white

[AWSS3-url]: https://aws.amazon.com/es/s3/

[AWSSES]: https://img.shields.io/badge/Aws%20SES-F8F9FA?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyBoZWlnaHQ9IjI5OSIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiIHZpZXdCb3g9IjAgMCAyNTYgMjk5IiB3aWR0aD0iMjU2IiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxwYXRoIGQ9Im02MC41NTYgNDcuNjAyLTYwLjU1NiA5Ni40MDggNjAuNTU2IDk2LjQyNCAxLjA1Ni0uNzUzLS43NzUtMTkxLjg4MXoiIGZpbGw9IiM4NzY5MjkiLz48cGF0aCBkPSJtMTI4LjE4NyAyMjMuMTA1LTY3LjYzMSAxNy4zMjl2LTE5Mi44MzJsNjcuNjMxIDE3LjMyNXoiIGZpbGw9IiNkOWE3NDEiLz48cGF0aCBkPSJtMjU1Ljk3OSA3MS44NjgtMzIuNiA1LjM5MS03NC44NDEtNzcuMjU5LTM3LjIwNyAxNi4yOTIgNC45MDggOS4xNTMtMjYuMzMzIDEwLjUyNnYyNDMuNDI4bDM4LjI4IDE5LjE1My42MzctLjQ5OS0uNTg5LTI1MC4yMzUgODEuMTQyIDEyMi45Njh6IiBmaWxsPSIjODc2OTI5Ii8+PGcgZmlsbD0iI2Q5YTc0MSI+PHBhdGggZD0ibTE0OC41MzggMCA5OS42NzkgNDkuODM3LTM5LjQxNyA3MS41MnoiLz48cGF0aCBkPSJtMjU1Ljk3NSA3MS44NjguMDI1IDE2Mi43MjgtMTI3LjgxMyA2My45NTYtLjAxNy0yNzcuODY5IDgwLjYzIDE0Ni4yOTF6Ii8+PC9nPjwvc3ZnPg==

[AWSSES-url]: https://aws.amazon.com/es/ses/

[WISE]: https://img.shields.io/badge/wise-9FE870?style=for-the-badge&logo=wise&logoColor=black

[WISE-url]: https://wise.com/es/

[POSTGRESQL]: https://img.shields.io/badge/postgresql-4169E1?style=for-the-badge&logo=postgresql&logoColor=white

[POSTGRESQL-url]:https://www.postgresql.org/