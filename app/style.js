import { StyleSheet } from 'react-native';

export default StyleSheet.create({
    screen: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    roundButton1: {
        width: 100,
        height: 100,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 10,
        borderRadius: 100,
        backgroundColor: 'orange',
    },
    roundButton2: {
        marginTop: 0,
        width: 200,
        height: 175,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 10,
        borderRadius: 100,
        backgroundColor: '#ccc',
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
    buttonContainer: {
        // flex: 1,
        padding : 5
    },
    gpsLabel: {
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#d3d3d3',
        padding: 10,
        marginHorizontal: 40,
        // margin: 15,
        marginVertical: 15,
        height: 80,
        borderRadius: 10
     },
     gpsText:{
        justifyContent: 'center',
        alignItems: 'center',
        color: 'white',
        fontSize: 25,
        height: 70
     }
});