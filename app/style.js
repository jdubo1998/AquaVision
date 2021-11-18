import { StyleSheet } from 'react-native';

export default StyleSheet.create({
    screen: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor:"#0b5394",
    },
    roundButton2: {
        marginTop: 0,
        width: 300,
        height: 200,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 10,
        borderRadius: 50,
        backgroundColor: '#0b5394',
    },
    roundButton3: {
        marginTop: 0,
        width: 300,
        height: 100,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 10,
        borderRadius: 50,
        backgroundColor: '#0b5394',
    },
    searchBar: {
        width: 50,
        padding: 10,
    },
    searchButton: {
        backgroundColor: 'orange',
        padding: '10px 20px',
        color: 'white',
    },
    searchForm: {
        minHeight: '10vh',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
    },
    container: {
        flexDirection: 'row',
        justifyContent: 'center',
    },
    container2: {
        alignSelf: 'stretch',
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
    },
    buttonContainer: {
        // flex: 1,
        padding : 5
    },
    gpsLabel: {
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#0b5394',
        padding: 10,
        marginHorizontal: 40,
        marginVertical: 15,
        height: 100,
        borderRadius: 10
     },
     connectionLabel: {
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#0b5394',
        padding: 10,
        marginHorizontal: 50,
        marginVertical: 15,
        flexDirection: 'row',
        height: 100,
        borderRadius: 10,
        marginHorizontal: 50,
     },
     socketLabel: {
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#0b5394',
        padding: 10,
        marginHorizontal: 50,
        marginVertical: 15,
        flexDirection: 'row',
        height: 100,
        borderRadius: 10,
        marginHorizontal: 50,
     },
     gpsText:{
        justifyContent: 'center',
        alignItems: 'center',
        color: 'white',
        fontSize: 25,
        height: 70
     },
     buttonText:{
         fontSize: 25,
         fontWeight: 'bold',
         color: 'white',
     }
});