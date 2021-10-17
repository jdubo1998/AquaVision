import React from 'react'
import { io } from 'socket.io-client';  

const socket = io('http://192.168.0.24:5000/') // Change to IP address of the device hosting the server.

/***   START OF TEST CODE (Unrefined code, just a way to get user's inputs for test chat.)  ***/
var message = {value: ''};
var inputComp = {comp: null}

function handleChange(e) {
    message.value = e.target.value;
    inputComp.comp = e.target;
}

export default function App() {
    console.log(socket)

    return (
        <div>
            <input type='text' onChange={(e) => handleChange(e)}/>

            <button onClick={relayMessage}>
                Send message.
            </button>
        </div>
    )
}

function relayMessage() {
    if (socket != null) {
        console.log(message.value);
        socket.emit('relaycommand', message.value); // Sends the string: message.value to the Command Module using even 'relaycommand'.
    }

    message.value = '';
    inputComp.comp.value = '';
}
/***   END OF TEST CODE   ***/

/* Event that triggers when the command that is sent to the Translate Module. */
socket.on('relaycommand', (command) => {})

/* Event that triggers when the data received from the Translate Module. */
socket.on('relaydata', (data) => {
    console.log(`Received data: ${data}`)
    // Do something with the data.
})

/* Event that triggers when a successful connetion is established. */
socket.on('connect', () => {
    console.log(`Connected with id: ${socket.id}`)
})

socket.on('connect_error', (err) => {
    console.log(err.message);
})

socket.on("disconnect", (reason) => {
    console.log(reason)
    /* If it was the server that disconnected, manually reconnect. */
    if (reason === "io server disconnect") {
        socket.connect()
    }
    // If it was not the server that disconnected, then it automatically reconnect.
})