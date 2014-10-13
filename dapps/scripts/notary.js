
//
// Notary
//

var Notary = function(options) {
  options = options || {};
  this.NOTARY = options.NOTARY || window.NOTARY;
  this.NOTARYDB = options.NOTARYDB || window.NOTARYDB;
};

Notary.prototype.messages = function() {
  var filter = {
    to: this.NOTARY
  };
  var messages = eth.messages(filter);
  return messages;
};

Notary.prototype.records = function() {
  var records = {};
  var messages = this.messages();
  for (var i = 0; i < messages.length; i++) {
    var m = messages[i];
    var command = param(m.input, 0);

    if (/^record/.test(command)) {
      var id = hex(param(m.input, 1), 20);
      var ID = '0x' + id + lpad('', 2*12);
      var owner = eth.stateAt(this.NOTARYDB, ID);
      if (owner != this.NOTARY)
        continue;

      var ACCOUNT = '0x' + id + lpad(hex("account"), 2*12);
      var TIMESTAMP = '0x' + id + lpad(hex("timestamp"), 2*12);
      var account = eth.stateAt(this.NOTARYDB, ACCOUNT);
      var username = str(namereg(account));
      var timestamp = int(eth.stateAt(this.NOTARYDB, TIMESTAMP));
      var record = {
        id: id,
        ID: ID,
        owner: owner,
        account: account,
        username: username,
        timestamp: timestamp,
        created_at: new Date(timestamp * 1000)
      };
      records[id] = record;
    }
  }
  return records;
};
