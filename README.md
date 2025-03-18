# Load Balancing Project

## Overview
This project implements a **Load Balancing** mechanism to efficiently distribute incoming requests across multiple resources to improve performance, reliability, and resource utilization. The system ensures that no single server is overwhelmed while others remain underutilized.

## Features
- **Dynamic Load Distribution**: Balances traffic across multiple servers based on real-time metrics.
- **Scalability**: Supports scaling up or down based on workload demands.
- **Failure Handling**: Detects and reroutes traffic from failed nodes.
- **Performance Optimization**: Reduces response time and prevents bottlenecks.
- **Algorithm Support**: Implements different load balancing strategies.

## Technologies Used
- **Programming Language**: Python
- **Frameworks**: Flask (for simulating servers)
- **Networking**: Nginx/HAProxy (for real-world implementation)
- **Monitoring Tools**: Prometheus, Grafana (optional for visualization)

## Installation & Setup
### Prerequisites
- Python 3.x
- pip (Python package manager)

### Steps to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/load-balancing.git
   cd load-balancing
   ```
2. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the simulated servers:
   ```bash
   python server.py 5001 &
   python server.py 5002 &
   ```
5. Run the Load Balancer:
   ```bash
   python load_balancer.py
   ```

## Project Structure
```
load-balancing/
│── load_balancer.py       # Main script
│── server.py              # Simulated backend servers
│── config.json            # Config for servers & strategy
│── requirements.txt       # Dependencies
│── README.md              # Documentation
│── venv/                  # Virtual environment (optional)
```

## Usage
- Modify `config.json` to set the number of servers and balancing strategy.
- Monitor performance via logs or integrated visualization tools.

## Future Improvements
- Support for AI-based predictive load balancing.
- Integration with cloud-based auto-scaling.
- Advanced monitoring and reporting tools.


