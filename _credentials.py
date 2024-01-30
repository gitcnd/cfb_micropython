# /_credentials.py

# To save:
#   In the web editor: Use ^s (ctrl-S)
#   In the "sh" (posix) edit command: Use ^s (ctrl-S) <enter> then ^q (ctrl-Q) <enter> to save then quit

__version__ = '1.0.1' # Major.Minor.Patch

HOSTNAME='esp32cam-cfb01' # Must  be a short mDNS-compatible name (no underscores, no dots, no special other than hyphen, must start+end with alphanumeric)

# List of WiFi credentials, ordered by preference.
# Each entry is a tuple containing the SSID and the corresponding password.
WIFI_CREDENTIALS = [
('cfb', 'your password here'),
('your home wifi here', 'and_password'),  # Note: 2.4ghz wifi only (ESP32 cannot see 5ghz networks)
('your phone hotspot wifi here', 'and_password'),
# Add more WiFi credentials as needed.
]

# To set the password below, run this code from the REPL >>>
# import gupy; gupy.passwd('set', 'MyNewPassword') # write new password into _credentials.py
PASSWORD="$5$bhICWllW9BZWmgICebx0aM2My9pqN5vw6as0UzCPpGo=$2nqD5qB/4X0hkB8oTKUlXdPIF3QgK/K9KN6/nG0gfqw=$" # unix shadow format (salted sha256)
# Note: above line is autogenerated from gupy.py