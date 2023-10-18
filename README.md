# Threads Clone Project

This project is a Threads clone that leverages React with TypeScript for the front end and Python with FastAPI for the back end.

## Table of Contents

- [Threads Clone Project](#threads-clone-project)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Technologies](#technologies)
  - [License](#license)

## Introduction

This project aims to replicate the core features of Threads using modern web development technologies. The front end is built using React with TypeScript, providing a seamless and efficient user experience. The back end is developed with Python using FastAPI, ensuring a robust and scalable server-side architecture.

## Features

- User authentication and authorization
- Tweet creation, deletion, and viewing
- User profile management
- Real-time updates using WebSockets

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd Threads-clone
2. Install dependencies for both the front end and back end:

   ```bash
   cd client
   npm install
   cd ../server
   pip install -r requirements.txt
3. Configure the environment variables:

      Create a .env file in the backend directory and add necessary environment variables such as API keys, database connection details, etc. 

4. Run the development server:
  
   Start the front end and back end development servers:
   Front end (TypeScript):

    ```bash
    cd client
    npm run dev
    ```
    Front end (TypeScript):

    ```bash
    cd server
    uvicorn main:app --reload
## Usage

1. Access the application via the provided URL or localhost depending on the configuration.
2. Sign up or log in to start using the Threads clone.
3. Explore, create tweets, manage your profile, and interact with other users.

## Technologies

- **Front End:**
  - React
  - TypeScript

- **Back End:**
  - FastAPI
  - PostgreSQL

## License

This project is licensed under the [MIT License](LICENSE).
