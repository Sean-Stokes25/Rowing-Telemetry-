# This file is executed on every boot (including wake-boot from deepsleep)

import network

# Create the Access Point interface
ap = network.WLAN(network.AP_IF)

# Turn the AP on
ap.active(True)

# Configure the AP
ap.config(
    essid="ESP32",
    password="12345678",
    authmode=network.AUTH_WPA2_PSK,
    channel=6,
    hidden=False,
    max_clients=4
)

#print IP info for debugging
print("SoftAP active")
print("AP IP config:", ap.ifconfig())
