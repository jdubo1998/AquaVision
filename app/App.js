import React from 'react'
import { io } from 'socket.io-client';  

const socket = io('http://localhost:5000')

export default function App() {
    console.log(socket)

    return (
        <body>
            safaf
        </body>
    )
}