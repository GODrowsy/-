
import time
from machine import Pin, UART
led=Pin(2,Pin.OUT)        #create LED object from pin2,Set Pin2 to output
Rout=Pin(4,Pin.OUT)
Rin=Pin(16,Pin.IN)
lock=Pin(17,Pin.OUT)
Buzzer=Pin(5,Pin.OUT)

uart = UART(2, baudrate=115200, rx=13,tx=12,timeout=10)
L=1
out = True
while True:
  uart = UART(2, baudrate=115200, rx=13,tx=12,timeout=10)
  if L == 0:
    lock.value(0)
    L=1
  print(uart.any())
  time.sleep(1)
  if uart.any():
    if uart.any()<=3:
      uart = UART(2, baudrate=115200, rx=13,tx=12,timeout=10)
      continue
    bin_data = uart.readline().decode()
    print('Echo String: {}'.format(bin_data))
    if bin_data == 'close':
      out = False
    elif bin_data == 'open':
      out = True 
    elif bin_data == 'lockon':
      lock.value(1)
      time.sleep(5)
      L=0
  while out:
    Rout.value(1)
    if Rin.value() == 1:
      print('cabinet off')
      led.value(0)
      Buzzer.value(0)
      time.sleep(0.5)
    elif Rin.value() == 0:
      print('cabinet on')
      led.value(1)
      Buzzer.value(1)
      time.sleep(0.5)
      
    if uart.any():
      bin_data = uart.readline().decode()
      print('Echo String: {}'.format(bin_data))
      if bin_data == 'close':
        out = False
      elif bin_data == 'open':
        out = True
      






