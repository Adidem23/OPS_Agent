# OPS Bot – Operational Intelligence Agent System

OPS Bot is an **AI-powered operational investigation system** designed for e-commerce platforms.  
It allows users to ask natural language questions about operational performance and automatically generates **deep operational insights, root cause analysis, and recommendations**.

The system uses a **multi-agent architecture with the A2A protocol** to coordinate specialized agents responsible for analytics, reasoning, and orchestration.

---

# Core Idea

OPS Bot enables queries such as:

```
Why are sales dropping in West India?
Why is Delhivery performing poorly in West India?
Why is SKU CBKSJ getting more returns?
```

The system automatically:

1. Extracts investigation scope
2. Runs deep analytics across operational tables
3. Explains root causes
4. Predicts operational risks
5. Produces a structured operational report

---

# Architecture Overview

```
User Query
    │
    ▼
Supervisor Agent
    │
    ▼
Analytics Fetcher Agent
    │
    ▼
Analytics Engine (SQL Investigation)
    │
    ▼
Analysis Runner Agent
    │
    ▼
Supervisor Final Insight
```

---

# Agents

## 1. Supervisor Agent

**Role:** Orchestration and final decision making.

Responsibilities:

- Receives the user query
- Delegates tasks to other agents
- Combines analytics insights
- Generates final operational report

Port:

```
8007
```

---

## 2. Analytics Fetcher Agent

**Role:** Extract investigation scope from natural language queries.

Example:

Input:

```
Why is Delhivery performing poorly in West India?
```

Output:

```json
{
  "region": "West India",
  "courier_name": "Delhivery"
}
```

Responsibilities:

- NLP query parsing
- Scope extraction
- Parameter validation

Port:

```
8009
```

---

## 3. Analysis Runner Agent

**Role:** Explain analytics results and generate operational insights.

Responsibilities:

- Interpret analytics output
- Identify operational signals
- Perform root cause reasoning
- Produce investigation reports

Port:

```
8010
```

---

# Analytics Engine

The analytics service performs **deep operational investigation across multiple data layers**.

Tables analyzed:

```
raw_order_events
raw_payment_events
raw_shipment_events
raw_inventory_events
raw_return_events
raw_user_events
```

Capabilities:

- Cross-table correlation
- KPI analysis
- Signal detection
- Operational breakdowns

Example output:

```
Shipment failures increased for Delhivery in West India
Payment failures increased by 12%
Checkout abandonment increased on mobile devices
```

---

# Database

Database used:

```
Supabase PostgreSQL
```

Tables simulate real e-commerce operational events.

| Table | Description |
|------|-------------|
| raw_order_events | Order lifecycle events |
| raw_payment_events | Payment transactions |
| raw_shipment_events | Courier delivery events |
| raw_inventory_events | Inventory changes |
| raw_return_events | Product returns |
| raw_user_events | User behavior |

---

# Synthetic Data Generator

The system includes a **data generator agent** that simulates operational activity.

It inserts randomized events into the database to mimic real e-commerce traffic.

Example events:

- order_created
- payment_failed
- shipment_dispatched
- stockout
- return_requested

---

# Technology Stack

| Component | Technology |
|----------|------------|
| Agents | A2A Protocol |
| AI Models | Gemini 2.5 Flash |
| Backend | FastAPI |
| Database | Supabase PostgreSQL |
| Analytics Engine | Python + SQL |
| Containerization | Docker |
| Async Communication | httpx + asyncio |

---

# Key Features

## Natural Language Operational Queries

Users can ask questions like:

```
Why are sales dropping in West India?
Why are payments failing in Mumbai?
Why is SKU CBKSJ getting more returns?
```

---

## Automated Root Cause Analysis

OPS Bot correlates signals across:

```
Orders
Payments
Logistics
Inventory
Returns
User Behavior
```

---

## Predictive Operational Insights

The system predicts potential operational risks such as:

- delivery failures
- payment disruptions
- increasing return rates
- declining conversion rates

---

## Multi-Agent Orchestration

Agents communicate through the **A2A protocol**, enabling modular AI services.

Benefits:

- scalable architecture
- agent specialization
- distributed reasoning

---

# Running the System

## 1. Install Dependencies

```
pip install -r requirements.txt
```

---

## 2. Start the Analytics Service

```
docker run -p 8006:8006 analytics_service
```

---

## 3. Start Agents

Run each agent in separate terminals.

Supervisor Agent

```
python agents/supervisor_node/__main__.py
```

Analytics Fetcher Agent

```
python agents/analytics_fetcher_node/__main__.py
```

Analysis Runner Agent

```
python agents/analysis_runner_node/__main__.py
```

---

# Testing the System

Example query:

```
Why is Delhivery performing poorly in West India?
```

Expected output:

```
Operational Investigation Report

Key Findings
Shipment failures increased for Delhivery in West India.

Operational Signals
Courier delivery failures increased significantly.

Root Cause Analysis
Delivery delays from the courier network are likely causing
increased order failures.

Operational Impact
Customers may experience delivery delays and order cancellations.

Predicted Risks
If the issue continues, fulfillment reliability may decline.

Recommended Actions
Investigate courier logistics routing and consider alternative
delivery partners.
```

---

# Example API Endpoints

Analytics Service

```
POST /analytics_engine/process
```

Agent Card Discovery

```
GET /.well-known/agent-card.json
```

---

# Project Structure

```
OPS_Bot
│
├── agents
│   ├── supervisor_node
│   ├── analytics_fetcher_node
│   ├── analysis_runner_node
│
├── analytics_service
│
├── data_service
│
├── database_schema
│
└── docker
```

---

# Future Improvements

Potential enhancements:

- real-time streaming analytics
- Redis caching layer
- anomaly detection models
- ML-based predictions
- automated operational alerts
- dashboard visualization

---

# Author

**Surya Suryawanshi**  
Software Engineer – HSBC Tech India  

Interested in:

- AI systems
- data engineering
- operational intelligence platforms
- multi-agent architectures
