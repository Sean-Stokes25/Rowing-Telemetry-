# Rowing-Telemetry-
My version of an NK speed-coach I guess

Trying to track distance,stroke-rate,speed, and create a graph of rate of acceleration per stroke.

Im using an esp32(Microcontroller),neo6m(GPS),BNO085(IMU) and ili9341(Display)

Esp32 reads the data from the sensors does the maths and diplays data on screen it also sends these numbers to ur phone using a local access point the range is about 40m.

This is just a project for me to become more comfortable with seriel and wireless communication (SPI and UART) although i do hope to be able to use it myself onec its is complete.


So far i have got distance and speed working
I have also got the access point working
Still messing around with fonts for my display (Im running out of ram)
im not going to start onto the IMU work(Rate, Distance per stroke and Acceleration graph) until i figure out my ram issue with the display
