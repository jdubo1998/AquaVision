# AquaVision
CSCE 483 Project 1

## Testing Socket.IO Communication
1. cd AquaVision\src\python
2. python3 .\server.py
3. *Copy the IP address that the server is running on.*
4. cd AquaVision\app
5. Edit App.js to match the IP address of server: 

**const socket = io('http://X.X.X.X:5000/')**

7. npx expo-cli start

## Testing GPS Module
1. cd AquaVision\src\python
2. python3 .\integration_testing.py (Tests both socket.io and GPS functionality.)
3. Run the react-native web app.
4. Press any button to update the GPS coordinates.
\
Notes:
The flask-socektio sever can only emit messages on the same thread that the server was initialized on. Because of this, I have not yet implemented a polling thread for the GPS module. Thus, only when the server receives a command does it run the code to get the GPS data.