# Real-Time Stock Market Data Streaming Pipeline

## Overview
This project builds a real-time data streaming pipeline using Kafka, Spark, InfluxDB and Grafana to process stock market data. The pipeline ingests live stock price updates, applies transformations, and stores the results for real-time monitoring and analytics. The goal is to handle high-throughput financial data efficiently while ensuring scalability and fault tolerance.

## Tech Stack
- **Data Collection:** Python using external API
- **Message Broker:** Apache Kafka
- **Data Processing:** Apache Spark (Structured Streaming)
- **Time-Series Storage:** InfluxDB
- **Visualization & Monitoring:** Grafana
- **Containerization & Deployment:** Docker, Docker Compose

## Architecture
1. **Data Source:** Fetches real-time stock market data from an external API.
2. **Kafka Producer:** Publishes stock price updates and trade data to Kafka topics.
3. **Kafka Broker:** Manages message distribution across consumers.
4. **Spark Structured Streaming:** Consumes, processes, and transforms stock market data in real time.
5. **Storage Layer:** Writes processed stock data to InfluxDB for efficient time-series storage.
6. **Dashboard:** Uses Grafana to visualize stock price trends, moving averages, and trade volumes.

**Note:** The project not only allows real-time stock price updates but also supports batch historical analysis.

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
[Demo Video](https://drive.google.com/file/d/1MLHAVVZpg3IgEZPkqJxF7O6Gpwr4KQOA/view?usp=sharing)