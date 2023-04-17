
# Raspberry_Pi_Pico_W_send_WoL

If you're trying to wake up a computer outside your LAN using WoL and having trouble, it might be because your router isn't broadcasting the magic packet to every device. Even if you port forward the necessary port, the packet might not reach the target computer. Here are a few things you can try:

1. Consider using a different router that supports Wake-on-LAN and can broadcast the magic packet to all devices on the network.

2. Alternatively, you can use a device that is always awake and can be accessed from outside the LAN to send the magic packet. For example, you could use a Raspberry Pi or a cloud server to send the packet on your behalf.

3. If all else fails, you could always physically go to the computer and press the button :)

Using solution 2 is a great option if you happen to have a Raspberry Pi Pico lying around since it consumes very little power. According to https://peppe8o.com/raspberry-pi-pico-w-power-consumption/, the power consumption of the Pico is minimal, making it an ideal device for this purpose.

Make sure you are using MicroPython.

You can follow [this steps to set up your Pico](https://projects.raspberrypi.org/en/projects/get-started-pico-w/0) 
