
/**
 * NotaryApp manages the notary demo page.
 *
 * @param {Notary} notary
 */

var NotaryApp = function(notary) {
  var self = this;
  self.notary = notary;
  self.init();
};

NotaryApp.prototype.init = function() {
  var self = this;
  $('#new-record').submit(function(event) {
    event.preventDefault();
    var $form = $(event.target);
    var hash = $form.find('[name=hash]').val();

    // Strip prefix, if present
    if (/^0x/.test(hash))
      hash = hash.substr(2);

    // Convert to hex, if necessary
    if (/[^0-9a-f]/.test(hash))
      hash = hex(hash, 20);

    self.notary.record(hash, function(err) {
      self.update();
    });
  });
  self.update();
};

NotaryApp.prototype.update = function() {
  var self = this;
  var records = self.notary.records();
  $('#records').empty();

  for (var id in records) { (function() {
    var record = records[id];
    var html =
      '<table class="record table">' +
      '  <tr><td>id</td><td><span class="record-id">' + record.id + '</span></td></tr>' +
      '  <tr><td>account</td><td><span class="record-account">' + record.account.substr(0, 10) + '...</span></td></tr>' +
      '  <tr><td>timestamp</td><td><span class="record-timestamp">' + record.timestamp + '</span></td></tr>' +
      '  <tr><td>username</td><td><span class="record-username">' + record.username + '</span></td></tr>' +
      '  <tr><td>created_at</td><td><span class="record-date">' + record.created_at.toISOString() + '</span></td></tr>' +
      '</table>' +
      '<a class="set-property" data-id="' + record.id + '" href="#">Set custom property</a>' +
      '<form class="new-property" role="form" style="display: none">' +
      '  <div class="form-group">' +
      '    <input class="form-control" name="key" placeholder="A 12-byte key">' +
      '    <input class="form-control" name="value" placeholder="A 32-byte value">' +
      '  </div>' +
      '  <button class="btn btn-primary" type="submit">Set property!</button>' +
      '</form>';
    var $elem = $(html);
    var $form = $elem.filter('.new-property');
    var $key = $form.find('[name="key"]');
    var $value = $form.find('[name="value"]');
    var $setProp = $elem.filter('.set-property');
    $setProp.click(function(event) {
      event.preventDefault();
      $form.toggle(150);
    });
    $form.submit(function(event) {
      event.preventDefault();
      var key = $key.val();
      var value = $value.val();
      self.notary.set(id, key, value, function(err) {
        self.update();
      });
    });
    if (record.account == eth.secretToAddress(eth.key)) {
      $setProp.show();
    }
    $('#records').append($elem);
  }()) }
};
