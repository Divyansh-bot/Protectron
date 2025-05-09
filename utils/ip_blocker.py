import subprocess

def block_ip(ip_address):
    """
    Blocks the given IP address using Windows Firewall.
    Requires the script to be run with administrator privileges.
    """
    try:
        rule_name = f"Protectron Block {ip_address}"
        result = subprocess.run(
            ["netsh", "advfirewall", "firewall", "add", "rule",
             f"name={rule_name}",
             "dir=in",
             "action=block",
             f"remoteip={ip_address}",
             "enable=yes"],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ Blocked IP: {ip_address}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to block IP: {ip_address}")
        print(e.output)
