import React, { useState } from 'react';
import { StyleSheet, Text, View, Button, LogBox, TouchableOpacity, TextInput } from 'react-native';
// ^^^ All these are libraries used to create the html objects below.
import { io } from 'socket.io-client';
import styles from './style.js';
import Icon from 'react-native-vector-icons/FontAwesome5' //this library has standard icons we used for the buttons

const socket = io('10.3.141.1:5000/') // Change to IP address of the device hosting the server.

export default function App() {
    const [gpsCoordinates, setGpsCoordinates] = useState("");
    const [connection, updateConnection] = useState("Disconnected");
    const [translate, updateTranslate] = useState("Disconnected");

    /***   Socket Functions   ***/
    /* Event that triggers when the command that is sent to the Translate Module. */
    socket.on('relaycommand', (command) => {})

    /* Event that triggers when the data received from the Translate Module. */
    socket.on('relaydata', (data) => {
        console.log(data)
        setGpsCoordinates(data)
    })

    /* Event that triggers when the data received from the Translate Module. */
    socket.on('handshake', (data) => {
        console.log(data)
        if (data == 'success') {
            updateConnection("Connected")
        }
    })

    /* Event that triggers when a successful connetion is established. */
    socket.on('connect', () => {
        console.log(`Connected with id: ${socket.id}`)
        updateTranslate("Connected")
    })

    socket.on('connect_error', (err) => {
        console.log(err.message);
        
    })

    socket.on("disconnect", (reason) => {
        console.log(reason)
        updateConnection("Disconnected")
        updateTranslate("Disconnected")

        /* If it was the server that disconnected, manually reconnect. */
        if (reason === "io server disconnect") {
            socket.connect()
        }
        // If it was not the server that disconnected, then it automatically reconnect.
    })

    return (
        //this div holds everything inside it
        <div>  
            {/* This VIEW object is a container for all the buttons. The reason its in a container is to style */}
            <View style={styles.gpsLabel}>
                <TouchableOpacity
                    onPress={getGPS}
                    style={styles.gpsLabel}>
                    <Icon size={24} color="white" name="map-pin"/>
                    <Text style={styles.buttonText}>GPS Coordinates</Text> 
                    <Text style = {styles.gpsText}
                    autoCapitalize = 'characters'

                    > {gpsCoordinates} </Text>
                </TouchableOpacity>
            </View>
            <View style={styles.container2}>
                <View style={styles.connectionLabel}>
                    <Text style={styles.buttonText}>WiFi Connection: {connection}</Text> 
                </View>
                <View style={styles.socketLabel}>
                    <Text style={styles.buttonText}>LoRa Connection: {translate}</Text> 
                </View>
            </View>
            <View style={styles.container}>
                {/* This view is a container for button 1 and is repeated below...*/}
                <View style={styles.buttonContainer}>
                    <TouchableOpacity
                        onPress={screenshotFunction}
                        style={styles.roundButton2}>
                        <Icon size={50} color="white" name="camera"/>
                        <Text style={styles.buttonText}>Screenshot</Text> 
                    </TouchableOpacity>
                </View>
                <View style={styles.buttonContainer}>
                    <TouchableOpacity
                        onPress={moveUpFunction}
                        style={styles.roundButton2}>
                        <Icon size={50} color="white" name="arrow-up"/>
                        <Text style={styles.buttonText}>Move Camera Up</Text> 
                    </TouchableOpacity>
                </View>
            </View>
            <View style={styles.container}>
                <View style={styles.buttonContainer}>
                    <TouchableOpacity
                        onPress={lightFunction}
                        style={styles.roundButton2}>
                        <Icon size={50} color="white" name="lightbulb"/>
                        <Text style={styles.buttonText}>Toggle Lights</Text> 
                    </TouchableOpacity>
                </View>
                <View style={styles.buttonContainer}>
                    <TouchableOpacity
                        onPress={moveDownFunction}
                        style={styles.roundButton2}>
                        <Icon size={50} color="white" name="arrow-down"/>
                        <Text style={styles.buttonText}>Move Camera Down</Text> 
                    </TouchableOpacity>
                </View>
            </View>
            <View style={styles.container}>
                {/* This view is a container for button 1 and is repeated below...*/}
                <View style={styles.buttonContainer}>
                    <TouchableOpacity
                        onPress={quitFunction}
                        style={styles.roundButton2}>
                        <Icon size={50} color="white" name="times"/>
                        <Text style={styles.buttonText}>Quit Program</Text> 
                    </TouchableOpacity>
                </View>
            </View>
        </div>
    )
    
    /***   Socket Functions   ***/
    /* Event that triggers when the command that is sent to the Translate Module. */
    function lightFunction() {
        socket.emit('relaycommand', 'lights');
    }

    function moveUpFunction() {
        socket.emit('relaycommand', 'moveup');
    }

    function moveDownFunction() {
        socket.emit('relaycommand', 'movedown');
    }

    function getGPS() {
        socket.emit('relaycommand', 'getgps');
    }

    function quitFunction() {
        socket.emit('relaycommand', 'quit');
    }

    function screenshotFunction() {
        socket.emit('relaycommand', 'screenshot');
    }
}
