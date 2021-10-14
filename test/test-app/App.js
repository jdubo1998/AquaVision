import React from 'react';
import { StyleSheet, Text, View, Button, LogBox } from 'react-native';
import { io } from "socket.io-client";

var message = {value: ''};
var inputComp = {comp: null}
var socket = null;

function handleChange(e) {
    message.value = e.target.value;
    inputComp.comp = e.target;
}

export default function App() {
  return (
      <div>
            <button onClick={testSocketConnection}>
                Test socket connection.
            </button>

            <input type='text' onChange={(e) => handleChange(e)}/>

            <button onClick={sendMessage}>
                Send message.
            </button>
      </div>
  );
}

function testSocketConnection() {
    console.log('Connection successful.');

    socket = io('128.194.50.17:8000');
    socket.on('connect', () => {
        console.log('Connected.');
    });

    socket.on('disconnect', () => {
        console.log('Disconnected.');
    });

    socket.on('relayCommand', (command) => {
        console.log(command);
    });
}

function sendMessage() {
    if (socket != null) {
        console.log(message.value);
        socket.emit(message.value);
    }

    message.value = '';
    inputComp.comp.value = '';
}
