function submit_register() {
  let register = $('#register_space');
  let data = extract_data(register);
  let lang = get_language();
  data['lang'] = lang;
  $.post('/frontend/register', data)
  .done(function (data) {
    if (data.status == "success") {
      display_message(data.statusmsg, "success");
      setTimeout(function () {
        location.href = "/"+lang+"/sign-in/";
      }, 5000);
    } else {
      display_message(data.errormsg, "fail");
    }
  })
  .fail(function (data) {
    data = data.responseJSON;
    display_message(data.msg, "fail");
  });
}

