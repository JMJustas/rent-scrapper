# rent-scrapper
Python script that scrapes Lithuanian apartment rental sites for cheapest offers.

# configuraton

Script is configured using config.json file that should be located at the same directory as script itself.

Example config:
```
{
    "sleep_time_max": 900,
    "email": {
        "to": "justinas.marcinka@gmail.com",
        "smtp": {
            "login": "jmmailerjm@gmail.com",
            "password": "sendmethatmail",
            "server": "smtp.gmail.com",
            "port": 587
        }
    },
    "search": {
        "max-price": 500
    }
}
```

- *sleep_time_max* Script maximum sleep time before execution. This sleep time is meant to make it harder to identify that this script is actually a bot. If set to 0, script will execute right away.
- *email* Email configurations:
  + *to* email address to which emails will be sent
  + *smtp* mail sender smtp configurations. 
- *search* Search filter configuration. Currently only max price is supported.
