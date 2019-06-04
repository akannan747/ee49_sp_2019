import network, time, machine

wlan = network.WLAN(network.STA_IF)      
wlan.active(True)
if wlan.isconnected():                   
    print("No WiFi Connection")
    # code to handle the problem ...
print("Connecting to Wifi ... ")
wlan.connect('EE49-2.4', '122Hesse', 5000)
#wlan.connect('Next time for sure though', 'Dontworryaboutit', 5000)

for _ in range(1000):                     
    if wlan.isconnected():
        print("Connected to WiFi!")
        break
    time.sleep_ms(100)
if not wlan.isconnected():               
    print("Unable to connect to WiFi")
    wlan.disconnect()      
    
machine.WDT(False)

rtc = machine.RTC()
rtc.ntp_sync(server="pool.ntp.org")
for _ in range(100):
    if rtc.synced(): break
    time.sleep_ms(100)
if rtc.synced():
    print(time.strftime("%c", time.localtime()))
else:
    print("Unable to get ntp time")