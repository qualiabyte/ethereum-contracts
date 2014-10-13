
//
// Helpers
//

// Contracts
var NAMEREG = '0x50441127ea5b9dfd835a9aba4e1dc9c1257b58ca';

// Reads storage value from NameReg
var namereg = function(key) {
  var value = eth.stateAt(NAMEREG, key);
  return value;
};

// Converts hex to int
var int = function(hex) {
  return parseInt(hex, 16);
};

// Converts hex to string
var str = eth.toAscii;

// Converts string to hex, right-padded with nulls
var zpad = eth.fromAscii;

// Converts string to hex, up to numBytes
var hex = function(str, numBytes) {
  numBytes = numBytes || 32;
  var digits = 2 * numBytes;
  var start = 2 + 64 - digits;
  return eth.fromAscii(str, 0).substr(start);
};

// Left-pads a string, to length with character
var lpad = function(str, len, char) {
  char = char || "0";
  while (str.length < len)
    str = char + str;
  return str;
};

// Right-pads a string, to length with character
var rpad = function(str, len, char) {
  char = char || "0";
  while (str.length < len)
    str += char;
  return str;
};

// Gets 32-byte parameter from transaction data
var param = function(data, index) {
  var offset = index * 32;
  var string = str(data).substr(offset, offset + 31);
  return string;
};

// Debug
var $debug = $('#debug');
var log = function() {
  for (i in arguments) {
    arg = typeof arguments[i] == 'string'
      ? arguments[i]
      : JSON.stringify(arguments[i], null, '  ');
    $debug.append(arg);
  }
  $debug.append('\n');
};
