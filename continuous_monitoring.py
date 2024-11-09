
# continuous_monitoring.py - Enhanced Continuous Monitoring Tool with Log Aggregation and Anomaly Detection

import json
import logging
import os
from datetime import datetime, timedelta
from logging_config import setup_logging

# Load configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Initialize logging
setup_logging("continuous_monitoring.log")
logger = logging.getLogger(__name__)

# Placeholder function to aggregate logs from configured sources
def aggregate_logs():
    aggregated_logs = []
    for source in config["log_aggregation"]["sources"]:
        if os.path.exists(source):
            with open(source, "r") as log_file:
                aggregated_logs.extend(log_file.readlines())
            logger.info(f"Aggregated logs from {source}")
        else:
            logger.warning(f"Log source {source} not found.")
    return aggregated_logs

# Function to analyze logs for anomalies based on configured thresholds
def detect_anomalies(logs):
    anomalies = []
    for log in logs:
        if "login_failure" in log:
            failure_rate = log.count("login_failure") / len(logs)
            if failure_rate > config["anomaly_detection"]["thresholds"]["login_failure_rate"]:
                anomalies.append("High login failure rate detected")
        if "data_transfer" in log:
            transfer_value = int(log.split("data_transfer:")[1].split()[0])
            baseline_value = transfer_value / config["anomaly_detection"]["thresholds"]["data_transfer_spike"]
            if transfer_value > baseline_value:
                anomalies.append("Data transfer spike detected")
    return anomalies

# Function to perform behavioral analysis and detect deviations from baseline
def analyze_behavior(logs):
    behavioral_issues = []
    baseline_date = datetime.now() - timedelta(days=int(config["behavioral_analytics"]["baseline_period"][:-1]))
    recent_logs = [log for log in logs if datetime.strptime(log.split()[0], "%Y-%m-%d") > baseline_date]

    if len(recent_logs) > 0.3 * len(logs):  # Arbitrary example deviation threshold
        behavioral_issues.append("Abnormal increase in recent activity")

    return behavioral_issues

# Function to send alerts based on detected issues
def send_alerts(issues, issue_type="anomaly"):
    if config["alerts"]["enable_real_time_alerts"] and issues:
        for issue in issues:
            alert_message = f"[{issue_type.upper()} ALERT] {issue}"
            logger.warning(alert_message)
            # Placeholder for actual alerting system (e.g., email or Slack)

# Main function to run continuous monitoring
def run_continuous_monitoring():
    logger.info("Starting Continuous Monitoring...")

    # Aggregate logs from configured sources
    logs = aggregate_logs()

    # Perform anomaly detection
    anomalies = detect_anomalies(logs)
    send_alerts(anomalies, issue_type="anomaly")

    # Perform behavioral analytics
    behavioral_issues = analyze_behavior(logs)
    send_alerts(behavioral_issues, issue_type="behavioral")

if __name__ == "__main__":
    run_continuous_monitoring()
