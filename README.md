# Mugiwara: Secure Banking System

## Introduction
Mugiwara is a secure banking system designed to provide a safe and reliable platform for managing user accounts, transactions, and payment requests. The system employs advanced security features, including OTP (One Time Password) verification, public key infrastructure (PKI), and HTTPS for secure communication.

## Features
### User Management
- **Registration**: Users can register by filling out a form. The registration request is reviewed and approved by an admin.
- **Login**: Users can log in to the system.
- **Profile Update**: Users can request to update their profile information. The update request is reviewed and approved by an admin.
- **Profile Deletion**: Users can request to delete their profile. The deletion request is reviewed and approved by an admin.

### Account Management
- **Create Account**: Users can request to create a new bank account. The request is reviewed and approved by an admin.
- **View Accounts**: Users can view their bank accounts.
- **Request Account Deletion**: Users can request to delete an account. The request is reviewed and approved by an admin.

### Transactions
- **Create Transaction**: Users can create a transaction (debit, credit, transfer) with OTP verification.
- **Approve Transaction**: Admins can approve or reject transaction requests.
- **View Transactions**: Users can view their transaction history.
- **Modify Transaction**: Users can request to modify a transaction amount. The request is reviewed and approved by an admin.

### Payment Requests
- **Submit Payment Request**: Users can submit payment requests. The request is verified using OTP and reviewed by an admin.
- **Approve Payment Request**: Admins can approve or reject payment requests.
- **View Payment Requests**: Users can view their payment requests.
- **Modify Payment Request**: Users can request to modify the amount in a payment request. The request is reviewed and approved by an admin.

## Security Features
- **OTP Verification**: Used for verifying user transactions and payment requests.
- **HTTPS with SSL/TLS**: Ensures secure communication between the server and clients.
- **Public Key Infrastructure (PKI)**: Used for securing communications and verifying identities.
- **Rate-Limiting**: Prevents brute force attacks by limiting login attempts.
- **CSRF Protection**: Ensures that requests are genuine and from the intended user.
- **X-Frame-Options**: Protects against clickjacking attacks.
- **Secure Cookies**: Ensures cookies are only sent over HTTPS connections.

## Technologies and Tools
- **Backend**: Django, Gunicorn
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: SQLite
- **Security**: HTTPS, SSL/TLS Certificates, mkcert, Let's Encrypt
- **Utilities**: Certbot, Virtualenv, Nginx

## Deployment
### Operating System
- **Ubuntu (Linux)**

### Server Setup
- **Nginx**: Used as a reverse proxy to serve the Django application.
- **Gunicorn**: WSGI HTTP Server for running the Django application.

### SSL/TLS Certificates
- **mkcert**: Used for generating local development certificates.
- **Let's Encrypt**: Used for obtaining trusted SSL/TLS certificates for production.

## Installation and Setup
### Prerequisites
- Python 
- Django 
- Virtualenv
- Nginx
- mkcert
- Certbot (for Let's Encrypt certificates)

### Steps
1. **Clone the Repository**
    ```bash
    git clone https://github.com/nikhil16kulkarni/Mugiwara
    cd Mugiwara
    ```

2. **Create and Activate Virtual Environment**
    ```bash
    python -m venv env
    source env/bin/activate
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up SSL Certificates**
    ```bash
    mkcert -install
    mkcert 127.0.0.1
    ```

5. **Configure Django Settings**
    - Update `settings.py` with your database configuration, allowed hosts, and security settings.

6. **Run Migrations**
    ```bash
    python manage.py migrate
    ```

7. **Create Superuser**
    ```bash
    python manage.py createsuperuser
    ```

8. **Collect Static Files**
    ```bash
    python manage.py collectstatic
    ```

9. **Run the Server Locally**
    ```bash
    python manage.py runserver_plus --cert-file 127.0.0.1.pem --key-file 127.0.0.1-key.pem
    ```

### Deploying on Ubuntu Server
1. **Install Nginx and Gunicorn**
    ```bash
    sudo apt update
    sudo apt install nginx
    pip install gunicorn
    ```

2. **Configure Nginx**
    - Create a configuration file in `/etc/nginx/sites-available/mugiwara` with the following content:
    ```nginx
    server {
        listen 80;
        server_name 156.56.103.247;

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /static/ {
            alias /home/mugiwara/Desktop/Mugiwara/static/;
        }

        location /media/ {
            alias /home/mugiwara/Desktop/Mugiwara/media/;
        }
    }
    ```

3. **Enable the Nginx Configuration**
    ```bash
    sudo ln -s /etc/nginx/sites-available/mugiwara /etc/nginx/sites-enabled/
    sudo systemctl restart nginx
    ```

4. **Run Gunicorn**
    ```bash
    gunicorn --certfile=156.56.103.247.pem --keyfile=156.56.103.247-key.pem --bind 127.0.0.1:8000 Mugiwara.wsgi:application
    ```

## Logging and Audit
- **Logging**: Configured to log errors and other information to a file (`debug.log`) for auditing purposes.
- **Secure Transactions Logging**: Logs all transactions and payment requests to enable external audits and ensure transparency.

## Development and Contribution
1. **Fork the Repository**
2. **Create a New Branch**
3. **Make Your Changes**
4. **Submit a Pull Request**

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

---

**Note:** This project is meant for educational purposes and may require additional security measures for production use.
