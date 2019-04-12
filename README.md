# twt-take-home

INSTRUCTIONS

download the repository and cd into the root directory ($twt)

run "python manage.py runserver"

accesible via http://localhost:8000/cars/overview/

the reset data button makes a new request to the mock api and updates the databases accordingly (takes a long time)

you can directly append the reset url to specify a comma separated list of countries to exclusively look at
example: http://localhost:8000/cars/reset/China,Russia,Jamaica

the search matches against makes,models,and countries

each of these have overview pages that list the total sales for that specific thing and a list of all their sales. 
