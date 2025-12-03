# dashboard-an6006

🚚 StreamLine Logistics: Modern Data Platform Design

AN6006 – Individual Assignment
Submitted by: Sumin Lee (MSc Business Analytics)

🔗 Real-Time Dashboard (Simulated Data)
https://glorious-space-giggle-pj69pq46qrr5crg6p-8502.app.github.dev/

1. Overview

StreamLine Logistics expanded from pallet shipping to high-volume parcel delivery. Their old on-premise SQL system cannot support the increased data volume, speed, and complexity. This results in system slowdowns, table locking, and unused IoT data.

This project analyzes the problem using the 5Vs framework and proposes a Modern Data Platform with real-time capabilities.

2. 5Vs Diagnosis (Summary)
Volume

85M+ rows in Orders

4TB of IoT JSON logs
→ System slows down during peak hours.

Velocity

450 trucks send data every 10 seconds

Daily report locks tables for 20 minutes
→ Real-time updates fail.

Variety

Structured SQL + IoT JSON
→ Current system cannot process both.

Veracity

GPS errors (“ghost points”)
→ No cleaning or validation pipeline.

Value

Empty truck returns, SLA penalties, rising fuel costs
→ Data not used for optimization.

3. Proposed Modern Architecture

The new platform includes:

CDC for real-time database updates

Streaming pipeline for IoT telemetry

Data Lake for raw and semi-structured data

Data Warehouse for analytics

Real-time processing for ETA, delays, and GPS cleaning

Dashboard layer for operations visibility

This design separates OLTP from analytics and supports real-time insights.

4. Real-Time Dashboard

🔗 Dashboard Link:
https://glorious-space-giggle-pj69pq46qrr5crg6p-8502.app.github.dev/

Features:

Live map of trucks

ETA and delay alerts

SLA risk monitoring

Pickup opportunities for empty trucks

The dashboard uses simulated data for demonstration.

5. Conclusion

The legacy SQL system cannot handle StreamLine’s modern parcel logistics. The proposed architecture uses streaming, CDC, a Data Lake, and real-time dashboards to improve performance and operational decision-making. This modern platform enables StreamLine to operate more efficiently and respond to issues in real time.