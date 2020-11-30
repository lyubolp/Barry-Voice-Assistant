### Register

Request to `/register`
```json
{
    email: "user@mail.com",
    password: "myPassword",
}
```

Response from `/register`
```json
{
    status: "success",
    token: "a665a4592042",
    errors: [],
}
```

### Login

Request to `/login`
```json
{
    email: "user@mail.com",
    password: "myPassword",
}
```

Response from `/login`
```json
{
    status: "success",
    token: "a665a4592042",
    errors: [],
}
```

### Execute

Request to `/execute?command=say&text=hello`
```json
{
    token: "a665a4592042"
}
```

Response from `/execute?command=say&text=hello`
```json
{
    status: "success",
    message: "Hello",
    details: {
        full_response: "Hello",
    },
    errors: [],
}
```

### List all configs

Request to `/list-config`
```json
{
    token: "a665a4592042"
}
```

Response from `/execute?command=say&text=hello`
```json
{
    status: "success",
    "global config": {
        city: "Sofia",
    },
    "user config": {
        google_api_key: "653a665a45a665a45",
        city: "London",
    },
    errors: [],
}
```

### Set config

Request to `/set-config?key=city&value=Sofia`
```json
{
    token: "a665a4592042"
}
```

Response from `/set-config?key=city&value=Sofia`
```json
{
    status: "success",
    errors: [],
}
```

### Get config

Request to `/get-config?key=city`
```json
{
    token: "a665a4592042"
}
```

Response from `/set-config?key=city`
```json
{
    status: "success",
    "global config": {
        city: "Sofia",
    },
    "user config": {
        city: "London",
    },
    errors: [],
}
```
