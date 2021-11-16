<?php

$pluginpath = "/wp-content/plugins/saasadmin/";
$lang = $_GET["lang"];

function loadTemplate($page)
{
    $template = file_get_contents("../templates/$page.html");

    $template = str_replace("{% csrf_token %}", "", $template);
    $template = str_replace("{% load i18n %}", "", $template);
    $template = str_replace("{{lang}}", $lang, $template);
    $template = str_replace('<script src="/static/', '<script src="'.$pluginpath, $template);

    while (($pos = strpos($template, "{% translate")) !== false) {
        $endpos = strpos($template, '%}', $pos) + 2;
        $startpos = strpos($template, '"', $pos) + 1;
        $caption = substr($template, $startpos, strrpos(substr($template, 0, $endpos), '"') - $startpos);
        // TODO: $caption = translate($caption, $lang);
        $template = substr($template, 0, $pos).$caption.substr($template, $endpos);
    }

    return $template;
}
?>
