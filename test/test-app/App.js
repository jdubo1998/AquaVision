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
    console.log('Conneciton successful.');

    socket = io('192.168.0.24:50422');
    socket.on('connect', () => {
        console.log('Connected.');
    });

    socket.on('disconnect', () => {
        console.log('Disconnected.');
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
