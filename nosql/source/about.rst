About
=====

Warning : This project is in development and not ready for production. The documentation is a work in progress. 
The document is rather a quick reminder than a full blown manual.

I attended a course, but I learn by doing. So I decided to create a project to apply the knowledge I gained.
The project is about investing in the stock market, but also about setting up Kubernetes, Docker, Helm, and other tools.

This project's data is real stockdata. 
The data is a large json object and stored in postgres as a JSONB field.

Container
----------

The software was packed in Docker containers.
This allows for deployment on a Kubernetes kluster as well. (helm script provided)


Visual
------- 

The data is accessible through a FASTAPI interface, and can be plotted.


Patterns
--------

As an investor, I'm interested in patterns. 
Three green periods, followed by a red one.
Reoccuring patterns, turnaround pattern ...


AI model
--------

synthetic data was used to create a keras model.
The purpose is to filter out similar patterns in the database. 

