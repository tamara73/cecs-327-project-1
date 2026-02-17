# Assignment 1: Mini Housing Search Service

This project is a small verions of an online housing search service. Users will be able to run a client program on their terminal and search for houses/apartments using city and maximum price as search attributes. 

## Description

Clients will be able to look through data from a JSON file. This program will also contain a:
1. Application server (server_app.py) which is what will go through clients queries applying the provided filters/requests by client by applying ranking and filtering additionally chaching recent results.
2. A data server (data_server.py) which will store the housing data and also answers simple data requests.

This is done through TCP ports using a 3 tier socket system which allows for communication between the programs. 

## Getting Started

### Installing & Dependencies

In order to run this program you will need Python 3.0 as well as 3 terminal windows for data_server.py, app_server.py, and client.py. You will also have to have the listings.json file in the same folder as the programs mentioned in order for the program to fetch the data for queries.

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)
