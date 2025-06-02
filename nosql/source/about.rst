About
=====

Warning : This project is in development and not ready for production. The documentation is a work in progress. 
The document is rather a quick reminder than a full blown manual.

I attended a course, but I learn by doing. So I decided to create a project to apply the knowledge I gained.
The project is about investing in the stock market, but also about setting up Kubernetes, Docker, Helm, and other tools.

This project fetches company data and stores it in a local database.
The data is a large json object and stored in postgres as a JSONB field.

selecting data
--------------

We are interested in the quarterly data for revenue and ROIC.
Our hypothesis is that these values are important drivers for the marketprice.
In order to prove this is the case, we extract marketcap as well.


reporting
---------

The data for revenue, ROIC, marketcap is stored in a pdf document, for each company.
Each quarter is displayed in a color (green, orange, red).
A criteria being used is the difference in percentage.


trader behaviour
----------------

In investing there a many strategies: Buy&Hold, buy the dip, technical analysis with RSI, SMA to determine buy&sell opportunities.
For this project we assume a selloff at a 8% drop.

patterns
--------

As an investor, I'm interested in patterns. 
Three green periods, followed by a red one.
Reoccuring patterns, turnaround pattern ...

