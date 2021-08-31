$.getScript("/static/js/utils.js", function (e) {
    lang=get_language();
    page="login";
    app="frontend";

    if (window.location.href.indexOf('/pricing') != -1) page="pricing";
    if (window.location.href.indexOf('/sign-in') != -1) page="login";
    if (window.location.href.indexOf('/register') != -1) page="register";
    if (window.location.href.indexOf('/pwd_reset') != -1) page="pwd_reset";
    if (window.location.href.indexOf('/confirm') != -1) page="confirm";
    if (window.location.href.indexOf('/account') != -1) page="account";
    if (window.location.href.indexOf('/product') != -1) page="product";
    if (window.location.href.indexOf('/payment') != -1) page="payment";
    if (window.location.href.indexOf('/sign-in') != -1) page="login";
    if (window.location.href.indexOf('/logout') != -1) page="logout";

    function loadPage(app, page,lang,plan) {
        $.get("/" + app + "/" + page + "?lang=" + lang + "&plan=" + plan, function(data) {
            if (data == "gotoAccount") {
                window.location.replace("/"+ lang + "/account");
            } else if (data == "gotoProduct") {
                window.location.replace("/" + lang + "/product");
            } else if (data == "gotoSignIn") {
                window.location.replace("/" + lang + "/sign-in");
            } else {
                $("#MyHTML").html(data);
            }
        });
    };

    plan = get_url_param("plan");

    loadPage(app, page, lang, plan);
});
