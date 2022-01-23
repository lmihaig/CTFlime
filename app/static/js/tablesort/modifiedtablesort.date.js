// modified by lmihaig

// YYYY-MM-DD HH-mm-ss to YYYY-MM-DDTHH-mm-ss
(function () {
  var parseDate = function (date) {
    date = date.replace(/\-/g, '/');
    date = date.replace(/(\d{2,4})[\/\-](\d{1,2})[\/\-](\d{1,2}) (\d{2}):(\d{2}):(\d{2})/, '$1-$2-$3T$4:$5:$6'); // format before getTime

    return new Date(date).getTime() || -1;
  };

  Tablesort.extend('date', function (item) {
    return (
      item.search(/\d{2,4}[\/\-]\d{1,2}[\/\-]\d{1,2} \d{2}:\d{2}:\d{2}/) !== -1
    ) && !isNaN(parseDate(item));
  }, function (a, b) {
    a = a.toLowerCase();
    b = b.toLowerCase();

    return parseDate(b) - parseDate(a);
  });
}());
