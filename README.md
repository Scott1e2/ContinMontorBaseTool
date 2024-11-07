# ContinMontorBaseTool
building a monitoring and baseline tool


# Continuous Monitoring 

## Overview
This Continuous Monitoring Tool is designed to track and maintain the effectiveness of security controls, compare their current state against a security baseline, and alert when deviations are detected. The tool supports third-party integrations (e.g., ServiceNow) to gather additional control data, ensuring comprehensive monitoring for internal and external compliance.

## Features
- **Baseline Comparison**: Continuously compares control statuses to a baseline defined in `baseline_config.json`.
- **Third-Party Integrations**: Connects to external APIs to retrieve control data (e.g., ServiceNow).
- **Incident Response and Drift Detection**: Triggers alerts on baseline violations, with basic incident response capabilities.
- **Modular Design**: Easily extendable to include additional controls, integrations, or response mechanisms.

## Requirements
- **Python 3.8+**
- **Python Libraries**: Install dependencies using `pip install -r requirements.txt`.
  - `requests`: For API calls to third-party services.

## Installation
1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-repository/continuous-monitoring-tool.git
    cd continuous-monitoring-tool
    ```

2. **Install Dependencies**:
    ```bash
    pip install requests
    ```

3. **Configure API Credentials**:
    - Update `monitor.py` with your actual API credentials and endpoint for third-party service integrations (e.g., ServiceNow or Splunk).

4. **Define Baseline Settings**:
    - Open `baseline_config.json` and customize it to reflect your organization’s security baseline. This file includes:
      - `expected_status`: Required state for each control.
      - `allowed_ports`: Expected open ports for firewall settings.
      - `max_failed_logins`: Acceptable threshold for failed login attempts before alerting.
      - `response_on_violation`: The action to take when a control deviates from the baseline (e.g., `alert`, `notify`).

    Example:
    ```json
    {
        "controls": {
            "firewall_rules": {
                "expected_status": "active",
                "allowed_ports": [80, 443, 22],
                "response_on_violation": "alert"
            },
            "authentication_service": {
                "expected_status": "healthy",
                "max_failed_logins": 5,
                "response_on_violation": "alert"
            }
        },
        "third_party_controls": {
            "service_now": {
                "expected_status": "compliant",
                "incident_threshold": 10,
                "response_on_violation": "notify"
            }
        }
    }
    ```

## Usage
1. **Run the Monitoring Tool**:
    ```bash
    python monitor.py
    ```

2. **Control Checks**:
    - The tool will perform control checks as defined in `monitor.py`:
        - **Firewall Rules**: Checks if current open ports match baseline settings.
        - **Service Health**: Verifies if critical services meet baseline health status.
        - **Third-Party Controls**: Queries a third-party API for control status and compares it to the baseline.

3. **Alerting and Response**:
    - Alerts are printed to the console when a control deviates from the baseline. The tool uses `response_on_violation` settings to determine the appropriate action (e.g., alerting, notifying an admin).
    - Example alert:
      ```
      [ALERT] Control check failed for: Firewall Rules
      ```

4. **Drift Detection**:
    - The tool tracks deviations over time. If a control frequently deviates from the baseline, it triggers a "drift detection" alert, suggesting that the control may need attention.

## Configuration
- **Frequency of Checks**: The tool is currently set to run every 5 minutes (configurable in `monitor_controls` function in `monitor.py`).
- **Custom Thresholds and Controls**: You can add new controls or adjust existing ones in `baseline_config.json` as needed.

## Extending the Tool
1. **Adding New Controls**:
    - Define new controls in `baseline_config.json` with expected states and acceptable thresholds.
    - Implement corresponding check functions in `monitor.py` to validate the control status and compare it to the baseline.

2. **Integrating Additional APIs**:
    - Update `query_third_party_controls` in `monitor.py` to connect to other third-party services as needed.

3. **Alerting via Email or Webhooks**:
    - Replace `alert_on_failure` in `monitor.py` with an email or webhook notification service to provide real-time alerts.

## Example Configuration and Alerts
- **Configuration Example**:
    ```json
    {
        "controls": {
            "data_encryption": {
                "expected_status": "enabled",
                "response_on_violation": "notify"
            },
            "user_access_policy": {
                "expected_status": "compliant",
                "response_on_violation": "alert"
            }
        }
    }
    ```
- **Sample Console Output**:
    ```
    Starting control checks against baseline...
    [ALERT] Control check failed for: Firewall Rules
    [DRIFT DETECTION] Control firewall_rules has deviated from baseline frequently.
    Control checks complete. Sleeping before next cycle...
    ```


