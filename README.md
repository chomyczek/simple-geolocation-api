# Simple Geolocation API

**Simple Geolocation API** is a lightweight microservice that provides geolocation information for a specified IP address or URL. The API accepts incoming requests and returns geolocation details—such as the continent, country, region, city, latitude, and longitude—in a structured JSON format. This project is designed for easy setup and integration into your applications, making it simple to look up physical location information based on an IP or URL.

---

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [API Routes](#api-routes)
  - [get](#get)
  - [add](#post)
  - [delete](#delete)
  - [responses](#responses)
- [Usage](#usage)

---

## Overview

The Simple Geolocation API is built to quickly fetch geolocation data for a given IP address or URL. It is meant to be simple to deploy, easy to integrate, and robust enough for lightweight production use. Under the hood, it leverages an SQLAlchemy-powered database for data persistence and may be extended to include caching or additional lookup services.

---

## Requirements
To run the application, you need to have an API key for the ipstack.com service.

---

## Installation

Follow these steps to set up the project locally.

1. **Clone the Repository:**

    ```bash
       git clone https://github.com/chomyczek/simple-geolocation-api.git
       cd simple-geolocation-api
    ```

2. **Set Up a Virtual Environment:**

   On Unix/macOS:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

    On Windows:
    ```bash
    python -m venv venv
    venv\Scripts\activate
   ```
3. **Install Dependencies:**

    Ensure you have pip installed and then run:
    
    ```bash
    pip install -r requirements.txt
   ```
   
---

## API Routes

### get

**Description:** Retrieve geolocation data already stored in database. You can supply either an IP address or a URL as a JSON input to look up its geolocation information.

#### Query Parameters:

- input : The IP or URL address to look up.

#### Example Request:

Example request
```bash
http://127.0.0.1:5000/add
```
Example body with IP
```json
{"input":"127.0.0.2"}
```
Example body with URL
```json
{"input":"www.example.com"}
```

### add

**Description:** Allows the creation of a new geolocation record. This route can be useful if you want to store or cache results obtained from external services.

#### Query Parameters:

- input : The IP or URL address to look up.

#### Example Request:

Example request
```bash
http://127.0.0.1:5000/add
```
Example body with IP
```json
{"input":"127.0.0.2"}
```
Example body with URL
```json
{"input":"www.example.com"}
```

### delete

**Description:** Deletes geolocation records based on the provided IP or URL identifier.

#### Query Parameters:

- input : The IP or URL address to look up.

#### Example Request:

Example request
```bash
http://127.0.0.1:5000/add
```
Example body with IP
```json
{"input":"127.0.0.2"}
```
Example body with URL
```json
{"input":"www.example.com"}
```

### Responses 
Returns a JSON object containing geolocation details and operation information:

- message: The information from the server about the status of the query.
- result(optional): The result object of the query.
    - city: The name of the city associated with the IP.
    - continent_name: The name of the country associated with the IP
    - country_name: The name of the country associated with the IP.
    - id: The object id related to database.
    - ip: The requested IP address.
    - latitude: The latitude value associated with the IP.
    - longitude: The longitude value associated with the IP.
    - radius: The radius in miles around an IP geolocation where the user is likely to be located. 
    - url(optional): The requested URL address.
    - zip: The ZIP code associated with the IP.

#### Example Request:
```json
{
    "message": "Value already in database.",
    "result": {
        "city": "Gdansk",
        "continent_name": "Europe",
        "country_name": "Poland",
        "id": 5,
        "ip": "127.0.0.2",
        "latitude": "54.319309234619141",
        "longitude": "18.637369155883789",
        "radius": "0E-10",
        "region_name": "Pomorskie",
        "url": "example.com",
        "zip": "80-009"
    }
}
```

---

## Usage

After installation, you can start the API with a simple command. For example:

```bash
python app.py -t <your-ipstack-key>
```

This will start the server, and you can interact with it at:
```
http://localhost:5000/
```

You can test the API endpoint using cURL, Postman, or by integrating it into your front-end application. Please see [Api Routes](#api-routes) section for example of usage. 
