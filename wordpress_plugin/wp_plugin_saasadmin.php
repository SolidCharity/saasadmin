<?php
/*
Plugin Name: SaasAdmin Plugin
Plugin URI: https://github.com/solidcharity/saasadmin/wordpress_plugin
Description: A simple wordpress plugin for inserting HTML code with shortcode for SaasAdmin
Version: 1.0
Author: Timotheus Pokorra
Author URI: https://www.solidcharity.com
License: GPL2
Version: 1.0.0
*/
/*
Copyright 2020-2021  Timotheus Pokorra  (email : timotheus.pokorra@solidcharity.com)

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License, version 2, as
published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/

if(!class_exists('PluginSaasAdmin')) :

	class PluginSaasAdmin
	{
        // insert the custom code for SaasAdmin
		public static function show() {
			$code = '<script type="text/javascript" src="/js/jquery.min.js"></script>'.
				'<link rel="stylesheet" href="/js/main.css"/>'.
				'<script src="/js/index.js" charset="utf-8"></script>'.
				'<div id="MyHTML"></div>';
			return $code;
		}
	}

function is_logged_in() {
	return is_page('account')
		|| is_page('product')
		|| is_page('payment')
		// the session variable does not work here???
		|| (($_SESSION != null) && in_array('saasadmin_logged_in', $_SESSION) && $_SESSION['saasadmin_logged_in']);
}

add_shortcode('op_insert_code', array('PluginSaasAdmin', 'show'));
endif;


