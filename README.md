# weatherAPI
Simple API to get weather information

Structure:
Database operations are under the DBOps class.
There are two models UserInfoModel and WeatherInfoModel to get input in a structured format.
Creating and validating token operations are under the Authenticate class.

How to run:
After docker container build, Container database.session.sql file should run to insert values to tables in database.
Then by running ready.py, the packages will be installed and API will start running on 127.0.0.1:8000.

Notes:
There is sample postman collection and API request/response template document that can be used for test.
