function submit_login() {
  let login = $('#login_space');
  let data = extract_data(login);
  let lang = get_language();
  $.post('/frontend/login', data)
  .done(function (data) {
    if (data.status=="success") {
      if (window.location.hostname.includes('saas')) {
        location.href = '/frontend/account';
      } else {
        location.href = '/'+lang+'/account/';
      }
    } else {
      display_message(data.errormsg, "fail");
    }
  })
  .fail(function (data) {
    data = data.responseJSON ? data.responseJSON : {};
    $('[name=password],[name=email]').css('background', '#fcc');
    $('[name=password]').val('').focus();
  });
}

