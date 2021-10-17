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
