"""Windows Admin Toolkit – reference solution
-------------------------------------------------
Requires **pywin32** (``pip install pywin32``) and works on Win10/11.

Implemented tasks (select with ``--task``):

* **win-events**       – failed & successful logons from the Security log
* **win-pkgs**         – list installed software (DisplayName + Version)
* **win-services**     – check service states; auto‑start if ``--fix`` flag supplied

Example runs
------------
```powershell
# Show IPs with ≥ 3 failed logons in last 12 h
python analyze_windows.py --task win-events --hours 12 --min-count 3

# Dump installed packages to a CSV
python analyze_windows.py --task win-pkgs --csv pkgs.csv

# Ensure Spooler & Windows Update are running (start them if stopped)
python analyze_windows.py --task win-services --watch Spooler wuauserv --fix
```
"""

import subprocess
import re
import argparse

def task_win_services():
    print("🩺 Service status")
    try:
        result = subprocess.run(["powershell", "-Command", "Get-Service | Select-Object -Property Name,Status"], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split('\n')[3:]  # skip header lines
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 2:
                name = parts[0]
                status = parts[-1]
                print(f"{name:20} {status}")
    except Exception as e:
        print(f"❌ Error getting services: {e}")

def task_win_events():
    print("📅 Recent System Events (Last 5)")
    try:
        result = subprocess.run(["powershell", "-Command",
            "Get-WinEvent -LogName System -MaxEvents 5 | Format-List TimeCreated,Message"], capture_output=True, text=True, check=True)
        print(result.stdout)
    except Exception as e:
        print(f"❌ Error getting events: {e}")

def task_win_startup():
    print("🚀 Startup Items")
    try:
        result = subprocess.run(["powershell", "-Command",
            "Get-CimInstance -ClassName Win32_StartupCommand | Select-Object Name,Command | Format-Table -AutoSize"], capture_output=True, text=True, check=True)
        print(result.stdout)
    except Exception as e:
        print(f"❌ Error getting startup items: {e}")

def task_win_firewall():
    print("🔥 Firewall Rules allowing inbound 0.0.0.0/0")
    try:
        result = subprocess.run(["powershell", "-Command",
            "Get-NetFirewallRule -Direction Inbound | Where-Object {($_ | Get-NetFirewallAddressFilter).RemoteAddress -eq '0.0.0.0/0'} | Get-NetFirewallRule | Select-Object DisplayName"], capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        if output:
            print(output)
        else:
            print("No inbound firewall rules found allowing 0.0.0.0/0.")
    except Exception as e:
        print(f"❌ Error getting firewall rules: {e}")

def task_win_tasks():
    print("⏰ Scheduled Tasks (non-Microsoft)")
    try:
        result = subprocess.run(["schtasks", "/query", "/fo", "LIST", "/v"], capture_output=True, text=True, check=True)
        output = result.stdout

        tasks = output.split("\r\n\r\n")
        count = 0

        for task_block in tasks:
            if not task_block.strip():
                continue

            name_match = re.search(r"TaskName:\s+(.+)", task_block)
            next_run_match = re.search(r"Next Run Time:\s+(.+)", task_block)

            if name_match and next_run_match:
                task_name = name_match.group(1).strip()
                next_run = next_run_match.group(1).strip()

                if not task_name.lower().startswith(r"\microsoft"):
                    print(f"{task_name:50} Next Run: {next_run}")
                    count += 1

        if count == 0:
            print("No non-Microsoft scheduled tasks found.")
    except subprocess.CalledProcessError:
        print("❌ Failed to query scheduled tasks. Try running as administrator.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Windows System Analyzer')
    parser.add_argument('--task', choices=['win-services', 'win-events', 'win-startup', 'win-firewall', 'win-tasks'], help='Specify the task to execute.')
    args = parser.parse_args()

    if args.task == 'win-services':
        task_win_services()
    elif args.task == 'win-events':
        task_win_events()
    elif args.task == 'win-startup':
        task_win_startup()
    elif args.task == 'win-firewall':
        task_win_firewall()
    elif args.task == 'win-tasks':
        task_win_tasks()
    else:
        print("Please specify a valid --task argument. Use -h for help.")

if __name__ == "__main__":
    main()