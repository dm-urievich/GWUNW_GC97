# GWUNW_GC97
Python code to get data from GWUNW GC97 battery capacity indicator
<img src='GWUNW-GC97-200V.png' width='200'>

Link to the device:
https://aliexpress.com/item/1005003378624928.html

GC97 is a coulumb counter battery capacity indicator. Evaluation of Li-ion (LiFePO4, Li-poly) battery charge based on battery voltage inaccurate. To get reamain capacity need to count income and outcome current, the difference is a battery charge.

Originally I used GC97 as battery capacity indicator on my DIY power station. Now that battery is an UPS (uninterruptible power source) for my smart home controller.

GC97 has an UART interface. Data avilable over UART:
   - battery voltage
   - battery current
   - battery power
   - charging state (current direction)
   - available battery charge in Ah and %
   - internal temperature
   - time since start of loading or charging

All data available over UART is shown on the GC97 display. There is no extra information. Also battery settings are not available over UART.

