#!/bin/bash



# Create Postgres Database with PSQL

# Variables
db_name="passport_office"
user="sysadmin"
password="passport"
host="127.0.0.1"
port="5432"
#postgres_user="postgres"

# password for postgres
export PGPASSWORD='password'

# password for sysadmin
#export PGPASSWORD=$password

## Create Database
psql -U postgres -h $host -p $port -c "CREATE DATABASE $db_name;"
##
### Create User
psql -U postgres -h $host -p $port -c "CREATE USER $user WITH PASSWORD '$password';"
##
### Grant Permissions
psql -U postgres -h $host -p $port -c "GRANT ALL PRIVILEGES ON DATABASE $db_name TO $user;"
##
#echo "Database $db_name created with user $user and password $password"

# Drop database
#psql -U postgres -h $host -p $port -c "DROP DATABASE $db_name;"

# Changing user password
#psql -U postgres -h $host -p $port -c "ALTER USER $user PASSWORD 'password';"

#psql -U postgres -h $host -p $port

#psql -U sysadmin -h $host -p $port -d $db_name
