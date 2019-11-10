const os = require('os');

var data = {};


// Get architecture 
data.arch = os.arch();

// Get information about each logical CPU core.
var cpus = os.cpus();

data.cpus = [];

for(var i = 0; i < cpus.length; i++) {
	data.cpus.push(cpus[i].model);
}

// Get Endianness 

data.endianness = os.endianness();

// Get Hostname 

data.hostname = os.hostname();

// Get Network interfaces 

data.network = os.networkInterfaces();

// Get platform 

data.platform = os.platform();

// Get OS Release

data.release = 	os.release();

// Get user info 

data.userinfo = os.userInfo();
console.log(data)
