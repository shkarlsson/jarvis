var dorita980 = require('dorita980');
console.log(`dorita980 version: ${require('dorita980/package.json').version}`);

console.log('Starting script...');
var blid = '3168411090527720'; // Ensure this is the correct blid
var addr = '192.168.1.58'; // Ensure this is the correct IP address
var pass = ':1:1718021841:2HZDmiuF2noI4Ypk'; // Ensure this is the correct password

console.log(`Using IP address: ${addr}`);
console.log(`Using BLID: ${blid}`);

var blid = '3168411090527720'; // Use the correct blid
var addr = '192.168.1.58'; // Use the correct IP address
var pass = ':1:1718021841:2HZDmiuF2noI4Ypk'; // Use the correct password

const net = require('net');

function checkRoombaAvailability(ip, callback) {
    const socket = new net.Socket();
    socket.setTimeout(3000); // 3 seconds timeout

    socket.on('connect', () => {
        callback(true);
        socket.destroy();
    }).on('error', () => {
        callback(false);
    }).on('timeout', () => {
        callback(false);
        socket.destroy();
    }).connect(8883, ip);
}
var reconnectAttempts = 0;
var maxReconnectAttempts = 5;
console.log(`Connecting with BLID: ${blid}, Password: ${pass}, IP: ${addr}`);
try {
    console.log(`Connecting with BLID: ${blid}, Password: ${pass}, IP: ${addr}`);
    var myRobot = new dorita980.Local(blid, pass, addr, { keepAlive: 10000 });
} catch (error) {
    console.error('Failed to instantiate dorita980.Local:', error);
    process.exit(1);
}


myRobot.on('connect', () => {
    console.log('Connected to the robot.');
    init();
});

myRobot.on('disconnect', () => {
    console.log('Disconnected from the robot.');
});

myRobot.on('reconnect', () => {
    if (reconnectAttempts < maxReconnectAttempts) {
        reconnectAttempts++;
        console.log(`Reconnecting to the robot... (Attempt ${reconnectAttempts}/${maxReconnectAttempts})`);
    } else {
        console.error('Max reconnect attempts reached. Please check your network and robot settings.');
        myRobot.end();
    }
});

myRobot.on('error', (err) => {
    console.error('Error:', err);
    if (err.message.includes('EHOSTUNREACH')) {
        console.error('Host unreachable. Please check the IP address and network connection.');
    } else if (err.message.includes('ECONNREFUSED')) {
        console.error('Connection refused. Please check if the Roomba is on and connected to the network.');
    } else {
        console.error('An unexpected error occurred:', err.message);
    }
});

function init() {
    console.log('Initialization starting...');
    myRobot.getRobotState()
        .then((time) => {
            console.log('Current time:', time);
            myRobot.end();
        })
        .catch(console.log);
}

checkRoombaAvailability(addr, (isAvailable) => {
    if (isAvailable) {
        console.log('Roomba is available on the network. Attempting to connect...');
        console.log('Please ensure the Roomba is on and connected to the network.');
    } else {
        console.error('Roomba is not reachable on the network. Please check the IP address and network connection.');
    }
});
