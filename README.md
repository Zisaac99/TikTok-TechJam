# Project for TikTok TechJam (Reshaping Payments - Wallets)

> ## Table of Contents

* [Overview](#Overview)
* [Features](#Features)
* [Tech Stack](#Tech-stack)
* [Getting Started](#Getting-Started)
  * [Prerequisites](#Prerequisites)
  * [API to run](#API-to-run)
* [Our Contributors](#Our-Contributors)

---

## Overivew
This project aims to showcase our team's idea to help the unbanked to go digital and to integrate this in their daily lives. We took inspiration from banking apps such as DBS/Standard Chartered to come up with our solution in the form of a webpage. 

## Features
- Security to ensure non-authorised personnel are not able to access the functions of the application
- See the transaction history of the user to help them to visualise their spending/earnings
- Transferring of funds to other users
- Withdrawal of funds at valid ATMs

## Tech Stack
- Flask
- Python
- HTML
- CSS
- Boostrap
- SqlAlchemy
- DataTables

## Getting Started
### Prerequisites
Here's what you need to run this project:
- Python 3.10

1. Clone the repository

```shell  
git clone https://github.com/Zisaac99/TikTok-TechJam.git
cd TikTok-TechJam
```

2. Create a virtual env

```shell  
python -m venv env
```

3. Activate the virtual env

```shell  
env\scripts\activate.hat
```

4. Install Dependecies

```shell  
pip install -r 'requirements.txt'
```

5. Set the Flask Application

```shell  
set FLASK_APP=app.py
```

6. Run the Application

```shell  
python =m flask run
```

7. Open the app in your browser

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

### API to run
#### Create ATM

`POST /api/add_atm?atm=<ATM Number>&withdraw=<Withdrawal Amount>`

    curl --location --request POST 'http://127.0.0.1:5000/api/add_atm?atm=1234&withdraw=200'

#### Response

    HTTP/1.1 201 Created
    Date: Thu, 6 Jul 2024 21:43:30 GMT
    Status: 201 Created
    Connection: close
    Content-Type: application/json
    Location: /api/add_atm?atm=1234&withdraw=200
    Content-Length: 85

    {"Success": "ATM: 123456 with max withdrawl amount of $200 was successfully created"}

### Our Contributors
<a href="https://github.com/Zisaac99/TikTok-TechJam/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Zisaac99/TikTok-TechJam" />
</a>
