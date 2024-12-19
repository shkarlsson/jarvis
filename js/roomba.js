var dorita980 = require('dorita980');

console.log('Starting script...');

var blid = '3168411090527720'; // Use the correct blid
var addr = '192.168.1.58'; // Use the correct IP address
var pass = ':1:1718021841:2HZDmiuF2noI4Ypk'; // Use the correct password

var myRobot = new dorita980.Local(blid, pass, addr);

myRobot.on('state', (state) => {
    console.log('Current state:', state);
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

console.log('Attempting to connect...');


myRobot.on('disconnect', () => {
    console.log('Disconnected from the robot.');
});

myRobot.on('reconnect', () => {
    console.log('Reconnecting to the robot...');
});
myRobot.on('connect', () => {
    console.log('Connected. Initializing...');
    init();
});
