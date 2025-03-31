# **Real-Time Stock Market Data Streaming Pipeline**

## **Prerequisites**
Before you begin, ensure you have met the following requirements:

- **Docker and Docker Compose** installed on your machine.
- **Stock symbols and necessary API keys** You need to set up an account in [ALPACA](https://alpaca.markets/) and obtain your API Key and API Secret Key.

## **Getting Started**
To get started with this project, follow these steps:

### 1. Clone the repository
```bash
git clone https://github.com/saikrishna-koppula/Docker-Kafka-Spark-InfluxDB-Grafana-Pipeline.git
```

### 2. Change to the project directory
```bash
cd Docker-Kafka-Spark-InfluxDB-Grafana-Pipeline
```

### 3. Set up environment variables
- Create a `.env` file in the project root directory and add the following:
  ```ini
  INFLUXDB_ADMIN_USER_PASSWORD=your_admin_password
  INFLUXDB_USER=your_username
  INFLUXDB_USER_PASSWORD=your_user_password
  INFLUX_TOKEN=your_influxdb_token
  ```
- Replace the placeholders with actual values.

Note: You can set the admin user and password as per your preference, these will be used to login for the first time to influxdb.

- **Ensure the `.env` file is not committed to version control** by adding it to `.gitignore`:
  ```bash
  echo ".env" >> .gitignore
  ```

### 4. Run the Docker Compose file
```bash
docker-compose up -d
```

### 5. Access the different services
- **Apache Kafka**: [http://localhost:9092](http://localhost:9092)
- **Apache Spark**: [http://localhost:8080](http://localhost:8080)
- **InfluxDB**: [http://localhost:8086](http://localhost:8086)
- **Grafana**: [http://localhost:3000](http://localhost:3000)

## **Project Structure**
The project structure is organized as follows:
```plaintext
Stock Market Project/           # Root directory of the project
│── CleanUp/                    # Scripts for cleaning up InfluxDB data
│── Consumer/                   # Consumer scripts to process data from Kafka
│── Docker_Files/               # Docker-related files for building images
│── Environment_Setup/Kafka/    # Kafka setup scripts and topics
│── Other_Testing/              # Testing scripts and sample data files
│── Producer/                   # Producer scripts to load stock and crypto data
│── Volumes/                    # Persistent storage for Grafana and InfluxDB
│── docker-compose.yaml         # Docker Compose configuration file
│── README.md                   # Project documentation and setup instructions
```

Follow these steps to deploy and monitor the real-time stock market data streaming pipeline successfully in your local system. 🚀
