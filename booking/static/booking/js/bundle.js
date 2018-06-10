
/*=============================================>>>>>
= Dynamic Inputs For Guests =
===============================================>>>>>*/

$(document).ready(function () {
  /* Clipboard Button Trigger */
  new ClipboardJS('.btn-clipboard');
});

/*= End of Dynamic Inputs For Guests =*/
/*=============================================<<<<<*/

/*=============================================>>>>>
= Surround Remove Anchor Styling =
===============================================>>>>>*/

$(document).ready(function () {

  $(".add-row").addClass("btn btn-sm btn-info mb-3 mt-3");
});
/*= End of Surround Remove Anchor Styling =*/
/*=============================================<<<<<*/

/*=============================================>>>>>
= Date Picker =
===============================================>>>>>*/
var today = new Date();
var tomorrow = new Date(today);
tomorrow.setDate(today.getDate() + 1);

var datepickerCheckIn = $('#id_check_in').datepicker().data('datepicker');
if (datepickerCheckIn != null) {
  datepickerCheckIn.update({
    position: "bottom right",
    minDate: today,
    todayButton: true,
    dateFormat: 'dd-mm-yyyy',
    language: 'en',
    autoClose: true

  });
}

var datepickerCheckOut = $('#id_check_out').datepicker().data('datepicker');
if (datepickerCheckOut != null) {
  datepickerCheckOut.update({
    position: "bottom right",
    minDate: tomorrow,
    todayButton: false,
    dateFormat: 'dd-mm-yyyy',
    language: 'en',
    autoClose: true
  });
}

$(document).on('click', '#id_check_out', function () {

  console.log(datepickerCheckIn);
});
/*----------- Number Of NIghts -----------*/

var _MS_PER_DAY = 1000 * 60 * 60 * 24;

// a and b are javascript Date objects
function dateDiffInDays(a, b) {
  // Discard the time and time-zone information.
  var utc1 = Date.UTC(a.getFullYear(), a.getMonth(), a.getDate());
  var utc2 = Date.UTC(b.getFullYear(), b.getMonth(), b.getDate());

  return Math.floor((utc2 - utc1) / _MS_PER_DAY);
}

difference = datepickerCheckIn['currentDate'].getUTCDay() - datepickerCheckOut['currentDate'].getUTCDay();

/*= End of Date Picker =*/
/*=============================================<<<<<*/
