
//
// Helpers
//

var Helpers = {};

// Contracts
Helpers.NAMEREG = '0x50441127ea5b9dfd835a9aba4e1dc9c1257b58ca';

// Reads storage value from NameReg
Helpers.namereg = function(key) {
  var value = eth.stateAt(NAMEREG, key);
  return value;
};

// Converts hex to int
Helpers.int = function(hex) {
  return parseInt(hex, 16);
};

// Converts hex to string
Helpers.str = function() {
  return eth.toAscii.apply(eth, arguments);
};

// Converts string to hex, right-padded with nulls
Helpers.zpad = function() {
  return eth.fromAscii.apply(eth, arguments);
};

// Converts string to hex, up to numBytes
Helpers.hex = function(str, numBytes) {
  str = str || '';
  numBytes = numBytes || str.length;
  var digits = 2 * numBytes;
  var start = Math.max(0, 64 - digits);
  var bytes = eth.fromAscii(str, 0).substr(2);
  return lpad(bytes, 64).substr(start);
};

// Left-pads a string, to length with character
Helpers.lpad = function(str, len, char) {
  char = char || "0";
  while (str.length < len)
    str = char + str;
  return str;
};

// Right-pads a string, to length with character
Helpers.rpad = function(str, len, char) {
  char = char || "0";
  while (str.length < len)
    str += char;
  return str;
};

// Strips characters from left end of string
Helpers.lstrip = function(str, char) {
  char = char || '0';
  return str.replace(new RegExp('^(' + char + '+)'), '');
};

// Strips characters from right end of string
Helpers.rstrip = function(str, char) {
  char = char || '0';
  return str.replace(new RegExp('(' + char + '+)$'), '');
};

// Strips characters from both ends of string
Helpers.strip = function(str, char) {
  return lstrip(rstrip(str, char), char);
};

// Gets 32-byte parameter from transaction data
Helpers.param = function(data, index) {
  var offset = index * 32;
  var string = str(data).substr(offset, offset + 31);
  return string;
};

// Gets 32-byte parameters from transaction data
Helpers.params = function(str) {
  var re = /(.{32})/g;
  var matches;
  var data = [];
  while (matches = re.exec(str))
    data.push(matches[1]);
  return data;
};

// Debug
Helpers.$debug = $('#debug');
Helpers.log = function() {
  for (var i in arguments) {
    arg = typeof arguments[i] == 'string'
      ? arguments[i]
      : JSON.stringify(arguments[i], null, '  ');
    $debug.append(arg);
  }
  $debug.append('\n');
};

$.extend(this, Helpers);
