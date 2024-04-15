---
date: 2024-04-15T18:08:28.293872
author: AutoGPT <info@agpt.co>
---

# q1

The Multi-Purpose API Toolkit is designed to be an extensive suite of powerful, single-endpoint APIs aimed at simplifying a variety of common tasks, thus providing developers with a versatile toolkit for different needs without requiring the integration of multiple third-party services. The toolkit encapsulates a broad spectrum of functionalities including QR Code Generation for seamless information sharing, Real-time Currency Exchange Rates to keep up with the financial market, IP Geolocation for acquiring detailed location data based on IP addresses, Image Resizing to adjust and optimize images dynamically, Password Strength Checking with suggestions for improvements, Text-to-Speech for converting text into natural audio outputs, Barcode Generation in various formats for inventory and tracking, Email Validation to enhance email deliverability, Time Zone Conversion for global timestamp accuracy, URL Preview to fetch and display web link metadata, PDF Watermarking for document protection and branding, and RSS Feed to JSON conversion for better content management and distribution. This all-in-one toolkit is engineered for simplicity and user-friendliness, targeting to streamline the developer's work by minimizing the need for deploying and managing multiple API solutions.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'q1'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
