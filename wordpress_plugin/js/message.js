// a global message that generates messages in the upper middle of the screen
function display_message(content, style_arguments, duration=5) {
  var display_space = $('#global_message_space');
  if (display_space.length == 0) {
    let x = $('<div id ="global_message_space" class="text-center" style="position:fixed;top:10vh;width:100%;z-index:5000;">');
    $('body').append(x);
  }
  var message = $('<div id="message" class="text-center msg" style="width:50%;margin:5px auto;cursor:pointer;" onclick="$(this).closest(\'.msg\').remove()">');
  message.addClass('display_message');

  if (style_arguments == null) {
    style_arguments = {};
  }

  // if 3rd arg is a pre definded option we add a class
  if (typeof style_arguments == "string") {
    if (style_arguments == "success") {
      message.addClass('display_message_success');
    }
    if (style_arguments == "fail") {
      message.addClass('display_message_fail');
    }
  } else {
    // if 2nd arg is object we add each item to style
    for (var arg in style_arguments) {
      message.css(arg, style_arguments[arg]);
    }
  }

  message.html(content);

  // need a random int to delete message
  var m_id = Math.floor(Math.random() * 100000);
  message.attr('message-id', m_id);

  $('#global_message_space').append(message);

  setTimeout(function () {
    $('[message-id='+m_id+']').remove();
  }, duration*1000);

}
