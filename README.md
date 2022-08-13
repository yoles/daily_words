# Boiler plate

Put within .envs/local/.env file:

```sh
    # DATABASE
    POSTGRES_NAME=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_HOST=db

    # APPLICATION
    SECRET_KEY=
    DEBUG=True

    # EMAIL
    EMAIL_HOST=my-host
    EMAIL_HOST_USER=my-user
    EMAIL_HOST_PASSWORD=my-passsword
    EMAIL_PORT=my-host-port
```

Then you could use 

```sh
    make init
```