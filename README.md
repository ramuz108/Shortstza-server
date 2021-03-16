# Shortstza-server
URL Shortener Server
Tools : Flask, Mysql

## Working
- Accepts the url in string format
- Returns the shortened url as the response
- Stores the shortened url into the database

## Features
- ### High Availability
    - Stores already shortened urls to the database and returns the response from the database when the same url is requested again reducing complexity and load.
    - A custom index is configured to the table for faster searches in case of frequent querying from the database
    - Application queries the internal database initially. If it finds the url not shortened earlier, then it communicates to an external api to shorten the url and once that endpoint is found to be down, the application switches and makes a request to the next external api.
- ### Flexible
    - Multiple external api endpoints are configured in the application.
    - Alternate external api gets called once the current one reflects an error or is experiencing downtime.
- ### Caching and Limiting
    - Frequently caches the server every 5 seconds to reduce heavy loads (just for demonstration)
    - Rate limits imposed on the API functions
- ### APIs Used
    - Bitly
    - Cutly
- ### Secure
    - Prepared statements are used for querying in the database
    - CORS configured locally
- ### Swagger Integration

## Excecution
  - ### Database Configuration
      - Upload and execute the **shortstza.sql** file to  any mysql server package in apache **(suggesting lamp or xampp)**
      - Change the database credentials in **server.py**
      - Start the database server
  - ### Dependencies
      - Open a terminal window in the directory and run `sudo pip3 install -r requirements.txt`
  ### Running the server
      - In the terminal window, run python3 server.py
      - Use Postman to make api calls externally if needed
  ### API docs
      - After running the server, navigate to `http://localhost:5000/apidocs/` for viewing the documentation and testing the apis
 ## Testing
   - To run unit tests, navigate to the tests directory and run `pytest -v` to initiate testing.
