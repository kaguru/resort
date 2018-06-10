$(document).ready(function () {
  $(".password-reset-form input#id_email").addClass('form-control col-md-9')
  .attr('placeholder', 'Enter Email Address');

  $(".password_reset_confirm #id_new_password1").addClass('form-control col-md-7')
  .attr('placeholder', 'New Password')
  .attr('autocomplete', 'off');

  $(".password_reset_confirm #id_new_password2").addClass('form-control col-md-7')
  .attr('placeholder', 'Confirm Password')
  .attr('autocomplete', 'off');
});
