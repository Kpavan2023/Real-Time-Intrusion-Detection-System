import subprocess
import re
import psutil
import sys
import os
import time

# Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from inference import predict_intrusion
except ModuleNotFoundError as e:
    print(f"\n❌ Import Error: {e}")
    print("🔍 Ensure 'inference.py' is inside 'backend/' and Python is running from 'backend' folder.")
    sys.exit(1)


def get_snort_interface():
    """
    Automatically detects the correct network interface for Snort.
    """
    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == 2 and addr.address.startswith("192.168"):  # Match local network
                return iface
    return "4"  # Default to interface 4 if no match


def capture_traffic(timeout=None):
    """
    Captures Snort alerts and processes them.
    """
    snort_interface = get_snort_interface()
    snort_cmd = fr"C:\\Snort\\bin\\snort.exe -i {snort_interface} -A console -q -c C:\\Snort\\etc\\snort.conf"
    
    print(f"\n🚀 Starting Snort on Interface: {snort_interface}")
    print(f"📌 Running Command: {snort_cmd}\n")

    try:
        process = subprocess.Popen(
            snort_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
            bufsize=1, universal_newlines=True
        )
        
        start_time = time.time()

        for line in iter(process.stdout.readline, ''):
            if timeout and (time.time() - start_time) > timeout:
                print("\n🛑 Timeout reached. Stopping Snort...")
                process.terminate()
                break
            
            decoded_line = line.strip()
            print(f"🐍 Raw Snort Output: {decoded_line}")  # Debugging Output
            
            if "alert" in decoded_line.lower():
                print(f"🚨 Snort Alert: {decoded_line}")
                handle_intrusion(decoded_line)
    
    except KeyboardInterrupt:
        print("\n🛑 Stopping Snort...")
        process.terminate()
    except Exception as e:
        print(f"\n❌ Error in Snort Capture: {e}")
    finally:
        process.wait()
        print("✅ Snort process terminated.")


def handle_intrusion(alert_info):
    """
    Handles intrusion events by extracting features and forwarding them to inference.
    """
    features = extract_features(alert_info)
    
    print(f"📊 Extracted Features: {features}")  # Debugging Log
    
    # Forward extracted features to AI model for final detection
    prediction = predict_intrusion(features)
    print(f"🔬 IDS Prediction Result: {prediction}")  # Log the prediction result


def extract_features(alert_info):
    """
    Extracts meaningful features from Snort alert logs.
    """
    ip_pattern = re.findall(r'\d+\.\d+\.\d+\.\d+', alert_info)
    src_ip = ip_pattern[0] if len(ip_pattern) > 0 else "0.0.0.0"
    dst_ip = ip_pattern[1] if len(ip_pattern) > 1 else "0.0.0.0"

    protocol = "TCP" if "TCP" in alert_info else "UDP" if "UDP" in alert_info else "ICMP"
    flag = "SYN" if "SYN" in alert_info else "ACK" if "ACK" in alert_info else "NONE"

    feature_vector = [
        hash(src_ip) % 1000,  # Hash IP to a numerical representation
        hash(dst_ip) % 1000,
        1 if protocol == "TCP" else 2 if protocol == "UDP" else 3,
        1 if flag == "SYN" else 2 if flag == "ACK" else 0
    ]

    return feature_vector


if __name__ == "__main__":
    capture_traffic(timeout=300)  # Run for 5 minutes then stop
