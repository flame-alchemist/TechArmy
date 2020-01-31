# TechArmy
Online Coding Platform

A complete application to host coding contests online, written in Python - Flask. UI - HTML, Javascript.

## Design
Consists of two micro services
  - Test : handles running the test cases for user written code (app.py)
  - User : handles adding new users, adding new contests, etc. (its.py)

Microservices can be scaled according to user traffic.

Communication - REST API

Database - MongoDB

## Test 
 - Application optimized to run all the test cases parallely using multiprocessing.
 - Shows user any kind of runtime/compilation errors.
 - Test can be taken in Python, C, C++, Java. 
 
## UI 
A web application, written in simple HTML, Javascript.
Pages to add users, host test, take test, generate report.

## Dependencies
 - Python 3
    - Flask
    - pymongo
 - gcc
 - jdk
