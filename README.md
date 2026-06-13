# ECFPv2

## Initial System Overview
A Discord-based system for tracking total and daily electricity consumption for Filipino users. The idea is that users upload images of their electric meters to a Discord bot and it gets read by an AI vision model (model depends on whether the input is a digital meter or analog meter). 

Information is stored in a database and the user is given the option to 
- Check average daily consumption
- Check estimated average daily expenses due to consumption
- Check how much more electricity/money did they save/use compared to last reading
- Compare consumption plots between different billing cycles

## Tech Stack & Design Philosophy
At its core, this project uses **Python 3** and **PostgreSQL 18** (running via Docker). Instead of using an ORM, I'm intentionally using raw SQL (`psycopg` v3) to handle the database interactions for learning purposes. 

## Current and Future Plans 
This project will likely end up as a combination of fullstack + AI vision + embedded development and will be a self-host type program. For now the plan is to focus on the backend (building out the core database logic and raw SQL queries) and AI vision component, and use a Discord bot as an interface.

## System Diagram
<img src="./media/architecture.png" />