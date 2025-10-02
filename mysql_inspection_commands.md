# MySQL Inspection Commands

## Connect to MySQL

mysql -u root -p

## Show all databases

SHOW DATABASES;

## Show tables in a database

USE database_name;
SHOW TABLES;

## Show all users

SELECT User, Host FROM mysql.user;

## Show grants/permissions for a user

SHOW GRANTS FOR 'username'@'host';

## Show current connections

SHOW PROCESSLIST;

## Show server version and status

SELECT VERSION();
STATUS;
