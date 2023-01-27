# Daily words

> Work in progress, but it is a low priority on my to do list.

DailyWord is an application that allows you to record words and their definitions. 
The principle is simple:
 - each day you can select a certain number of words you want to play and find their definition.
 - At the end of the game you have the summary of what you have found or not.

# Words found

The words found will be proposed to you 1 day later to consolidate your knowledge.
Each time you succeed, the word will be proposed to you again within a timeframe that varies:
1 success = 1 day later
2 success = 2 days later
3 success = 5 days later
4 success = 15 days later
5 success = 30 days later
6 success = 6 months later
7 success = 12 months later

# Words not found
The words you got wrong are returned to the list of words to play today.
If you were in "series", the word goes down one category.

# Notification

You will receive one notification per day as a reminder to do your words.
Fully configurable: 
- by sms or email
- selection of a reminder time slot
- can be deactivated according to the period


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
