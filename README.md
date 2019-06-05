# Simple Payment System

Simple web application on Django which allows to:
- register a client wallet with specified currency
- fill up a wallet
- transfer assets to other wallets
- update currency exchange rate (based on USD)
- get report about log of transfers of a wallet (with optional CSV export) in specified period

# How to install
0. pull the code from git:
`git clone https://github.com/acriptis/django_simple_payment_system django_simple_payment_system`
1. Create a virtual environment and launch it:
`virtualenv -p python3 .venv`
`source .venv/bin/activate`
2. cd to project root directory of the project
3. Install requirements:
`pip install -r requirements.txt`
4. Initialise Database:
`python manage.py migrate`
5. Load fixtures with sample data (Admin User/Exchenage Rates/Wallets/Users/Transactions):
`python manage.py loaddata wallets/fixtures/initial_dump.json`
6.Now you can start a test server:
`python manage.py runserver`
7. Enjoy:
http://127.0.0.1:8000/wallets/
http://127.0.0.1:8000/admin/

# Links to useful resources in topic:
https://github.com/django-money/django-money
https://github.com/fusionbox/dinero
https://medium.com/coinmonks/step-by-step-guide-to-programming-your-own-bitcoin-wallet-9d38942c8ae0
https://github.com/SmileyChris/django-countries


Draw io diagram:
https://www.draw.io/#G1_rKKi_I-x_WOHOofHNdqmYX3uJLNEe3E