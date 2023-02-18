# canto-etl

ETL of Canto data into a relational database. 

### instructions

this repo was intended to be the easiest way to bootstrap a basic Canto data warehouse. It is not intended to be a production ready solution. 

### setup

1. clone this repo.
2. run the addresses.py script until it completes successfully. as of feb. 17, 2023, the number of addresses is ~140,000.
3. run the transactions.py script and tokentx.py script until they complete. these scripts scrape the canto evm block explorer api for all transactions and token transfers. note: if you are getting json formatting errors, try removing the brackets '[]' outside of from the end of the json files. 
4. convert the json files to csv files. you can use the json_to_csv.py script to do this.
5. create the schemas in the /schema_creation directory in your database of choice. the schema creation directory contains the sql files for postgres, you might have to modify these sql files for your database of choice. note: loading data depends on the dbms you use. for postgres, you can use the COPY command to load data from csv files. 
6. run the create canto_activities_view sql file last. if you want to modify the schema, you can do so here, picking and choosing which columns you want to include in the view.
7. you now have a relational database with transaction and token transfer and address data which you can use to run analytical queries on the canto blockchain.

### next steps

1. modify this repo to use the canto rpc api instead of the evm block explorer api - this will be much faster and more sustainable
2. add live updates to the database using the canto rpc api 
3. set up scripts using a database like supabase to reduce set up time