function get_language() {
  var lang="en";
  if (window.location.href.indexOf('/de/') != -1) lang="de";
  return lang;
}

function get_url_param(name) {
  var results = new RegExp('[\?&]' + name + '=([^&]*)').exec(window.location.href);
  if (results==null){
   return null;
  }
  else{
   return results[1] || 0;
  }
}

function extract_data(jquery_object) {

  let result = {};
  for (space of jquery_object.find('[name]')) {
    let field = $(space);
    if (field.attr('type') == "checkbox") {
      if (field.is(':checked')) {
        result[field.attr('name')] = true;
      } else {
        result[field.attr('name')] = false;
      }
    } else if (field.attr('type') == "radio") {
      if (field.is(':checked')) {
        result[field.attr('name')] = field.val();
      }
    } else {
      result[field.attr('name')] = field.val();
    }
  }
  return result;
}

function insert_data(jquery_object, data) {

  for (k in data) {

    let r = jquery_object.find("[name="+k+"]");
    if (r == null) { continue }

    r.val(data[k]);

  }

  return jquery_object;

}

function format_date(date, format) {

  let f = {};

  f["dd"] = String(date.getDate()).length > 1 ? String(date.getDate()) : "0"+String(date.getDate());
  f["mm"] = String(date.getMonth()+1).length > 1 ? String(date.getMonth()+1) : "0"+String(date.getMonth()+1);
  f["yyyy"] = String(date.getFullYear());

  for (var piece in f) {
    format = format.replace(piece, f[piece]);
  }
  return format;

}

function logout() {
  $.post('/frontend/logout').
  done(function (data) {
    location.reload();
  })
}
