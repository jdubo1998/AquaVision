import React from 'react'
import { io } from 'socket.io-client';  

const socket = io('http://127.0.0.1:5000')

export default function App() {
    console.log(socket)

    return (
        <div>
            safaf
        </div>
    )
}

socket.on('connect_error', (err) => {
    console.log(err.message);
 })