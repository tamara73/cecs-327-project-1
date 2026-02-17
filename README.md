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

This system uses a 3-tier architecture and must be started in the correct order.

You will need **three terminal windows**.

#### Step 1: Navigate to the project folder
In each terminal, move to the folder that contains the project files:

```
cd path/to/your/project
```

#### Step 2: Run all 3 python files
In each terminal you will run one python script in the order:
```
python data_server.py
```
```
python app_server.py
```
```
python client.py
```
#### Step 3: Make a query request
Follow the inctructions provided by each python file in the terminal. You will be able to make a query in the client.py terminal. 
To quit simply enter "quit" into the terminal and enter. Alternatively you can also use Ctrl + C.


## Authors

Ashley Garcia, Melanie Cativo, Kimberly Martinez Cardoso

## Course and University
CECS 327 - California State University, Long Beach - 02/17/2026
