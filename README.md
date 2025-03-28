# Real-Time Stock Market Data Streaming Pipeline

## Overview
This project builds a real-time data streaming pipeline using Kafka, Spark, InfluxDB and Grafana to process stock market data. The pipeline ingests live stock price updates, applies transformations, and stores the results for real-time monitoring and analytics. The goal is to handle high-throughput financial data efficiently while ensuring scalability and fault tolerance.

## Tech Stack & Architecture
- **Data Collection:** Python using external API to fetch real-time stock market data.
- **Message Broker:** Apache Kafka, which manages message distribution across consumers.
- **Data Processing:** Apache Spark (Structured Streaming) for consuming, processing, and transforming stock market data in real time.
- **Time-Series Storage:** InfluxDB, used to store processed stock data efficiently.
- **Visualization & Monitoring:** Grafana, which visualizes stock price trends, moving averages, and trade volumes.
- **Containerization & Deployment:** Docker and Docker Compose for containerization and deployment of the system.

**Note:** The architecture not only allows real-time stock price updates but also supports batch historical analysis.

## Lessons Learned & Future Improvements
### Lessons Learned
- Fine-tuning Kafka and Spark configurations is critical for efficiency.
- Proper data partitioning prevents bottlenecks.
- Real-time monitoring enhances system observability and debugging.

### Future Improvements
- Integrate Kafka Streams for real-time financial calculations (e.g., VWAP, RSI).
- Use machine learning models for stock price anomaly detection.
- Improve Grafana dashboards with more financial indicators and alerts.

## Conclusion
This project demonstrates a scalable and fault-tolerant approach to real-time stock market data streaming. By leveraging Kafka, Spark, and InfluxDB, it ensures reliable message processing, efficient storage, and real-time visualization using Grafana. The architecture supports high-frequency trading environments and is adaptable for advanced financial analytics.

## Additional Links
- [Demo Video](https://drive.google.com/file/d/1MLHAVVZpg3IgEZPkqJxF7O6Gpwr4KQOA/view?usp=sharing)
- [Challenges Encountered and Solutions Implemented](./Challenges.md)