# Project Nigel

This will be the repo for all Project Nigel related code.

## Solutions
 - "Nigel's brain"
    - Python
    - Capturing microphone input and turning it into text
    - Intent detection on the text to determine what action to take
    - Send required information to the "face" to display
    - Take action based on intent
    - Websocket connection with "face" at all times
    - Configuration that can be changed by websocket
    - Robust libraries that allow for easy interaction with hardware. (make a library for each attachment) 
 - "Nigel's Neurons"
    - Typescript
    - Literally just hosts the websocket server as we can't guarentee that the brain will have port forwarding to host it.
    - Will just forward messages
 - "Nigel's face"
    - The face will be a website visited by any device
    - React
    - Display information such as subtitles for what nigel is saying on screen
    - Change config(e.g default music provider)
    - Soundboard page
