var dorita980 = require('dorita980');

console.log('Starting script...');

// Dobby
var blid = '31C7C41471534660'
var pass = ':1:1638469508:v7WJLmtq9Le7pcwJ'
var addr = '192.168.1.50'

// Kreacher
var blid = '3168411090527720'
var addr = '192.168.1.58'
var pass = ':1:1718021841:2HZDmiuF2noI4Ypk'

var myRobot = new dorita980.Local(blid, pass, addr);


myRobot.on('error', (err) => console.error('Error:', err));


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
myRobot.on('connect', () => {
    console.log('Connected. Initializing...');
    init();
});
