# Anomaly Detection on Event Rates 

This project focuses on detecting anomalies in event rates using the Isolation Forest algorithm. It leverages Docker for environment isolation and pytest for testing functionalities of the code.

## Overview

- **Algorithm**: The code use Isolation Forest for detecting anomalies. ( Threshold 10 precent )
- **Running**: start main.py to process all data and show all anomalities in a graph.
- **Testing**: for testing use docker enviorment to simulate working against elasticsearch and testing all functionalities of anomaly_count.py

## About the Algorithm

Isolation Forest is an unsupervised learning algorithm for anomaly detection. It works on the principle of isolating anomalies based on the fact that anomalies are data points that are few and different. This makes anomalies more susceptible to isolation.

Advantages:

- Unsupervised Algorithm.
- Time Complexity O(nlogn) - Faster than most anomalities detection algorithms.
- Simple to use and handle.


