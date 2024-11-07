
import requests
import time
import json

# Load baseline configuration
with open('baseline_config.json', 'r') as baseline_file:
    baseline_config = json.load(baseline_file)

API_ENDPOINT = "https://api.thirdpartyservice.com/controls"
API_KEY = "your_api_key_here"

# Check if firewall rules match the baseline
def check_firewall_rules():
    print("Checking firewall rules...")
    expected_ports = baseline_config['controls']['firewall_rules']['allowed_ports']
    # Example check for open ports (replace with actual port scanning code)
    open_ports = [80, 443]
    if all(port in expected_ports for port in open_ports):
        return True
    else:
        return False

# Check service health based on baseline
def check_service_health(service_name):
    print(f"Checking health of service: {service_name}")
    # Simulated service status
    service_status = "unhealthy"  # example value
    max_failed_logins = baseline_config['controls']['authentication_service']['max_failed_logins']
    if service_status == baseline_config['controls']['authentication_service']['expected_status']:
        return True
    else:
        return False

# Query third-party controls and check if they comply with baseline
def query_third_party_controls():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        response = requests.get(API_ENDPOINT, headers=headers)
        if response.status_code == 200:
            controls_data = response.json()
            print("Retrieved third-party control data.")
            for control in controls_data:
                expected_status = baseline_config['third_party_controls']['service_now']['expected_status']
                if control.get("status") != expected_status:
                    alert_on_failure(control.get("name", "Unnamed Third-Party Control"))
            return controls_data
        else:
            print("Failed to retrieve control data.")
            return None
    except Exception as e:
        print(f"Error connecting to third-party API: {e}")
        return None

# Alert function to notify on failed control checks
def alert_on_failure(control_name):
    print(f"[ALERT] Control check failed for: {control_name}")
    # Incident response logic based on baseline response
    response_action = baseline_config['controls'][control_name].get('response_on_violation', 'alert')
    if response_action == "notify":
        print(f"Notifying admin of failure in control: {control_name}")

# Function for detecting drift over time (simple counter for demonstration)
drift_count = {}
def detect_drift(control_name, status):
    if control_name not in drift_count:
        drift_count[control_name] = 0
    if not status:
        drift_count[control_name] += 1
    if drift_count[control_name] > 3:
        print(f"[DRIFT DETECTION] Control {control_name} has deviated from baseline frequently.")

# Monitoring loop to compare against baseline and run checks
def monitor_controls():
    while True:
        print("Starting control checks against baseline...")

        # Internal controls
        if not check_firewall_rules():
            alert_on_failure("firewall_rules")
            detect_drift("firewall_rules", False)

        if not check_service_health("authentication_service"):
            alert_on_failure("authentication_service")
            detect_drift("authentication_service", False)

        # Query third-party controls
        query_third_party_controls()

        print("Control checks complete. Sleeping before next cycle...")
        time.sleep(300)  # Run every 5 minutes

if __name__ == "__main__":
    monitor_controls()
