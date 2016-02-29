(function(){

	// the minimum version of jQuery we want
	var v = "1.3.2";

	// check for jQuery. if it exists, verify it's not too old.
	if (window.jQuery === undefined || window.jQuery.fn.jquery < v) {
		var done = false;
		var script = document.createElement("script");
		script.src = "http://ajax.googleapis.com/ajax/libs/jquery/" + v + "/jquery.min.js";
		script.onload = script.onreadystatechange = function(){
			if (!done && (!this.readyState || this.readyState == "loaded" || this.readyState == "complete")) {
				done = true;
				initMyBookmarklet();
			}
		};
		document.getElementsByTagName("head")[0].appendChild(script);
	} else {
		initMyBookmarklet();
	}
	
	function initMyBookmarklet() {
		(window.myBookmarklet = function() {
			if ($("#trayframe").length == 0) {
					$("body").append("\
					<div id='trayframe'>\
						<div id='trayframe_veil' style=''></div>\
						<iframe src='http://{{bookmarklet_domain}}/add-item?link="+location.href+"&title="+document.title+"&bookmarklet_key={{bookmarklet_key}}' onload=\"$('#trayframe iframe').slideDown(500);\">Enable iFrames.</iframe>\
						<style type='text/css'>\
							#trayframe_veil { display: none; position: fixed; width: 100%; height: 100%; top: 0; left: 0; background-color: rgba(255,255,255,.25); cursor: pointer; z-index: 900; }\
							#trayframe iframe { display: none; position: fixed; top: 0; left: 0; width: 100%; height:125px; z-index: 999; border:none; margin: 0; }\
						</style>\
					</div>");
					$("#trayframe_veil").fadeIn(750);
				}
			$("#trayframe_veil").click(function(event){
				$("#trayframe_veil").fadeOut(750);
				$("#trayframe iframe").slideUp(500);
				setTimeout("$('#trayframe').remove()", 750);
			});
			function receiveMessage(event){
  				if (event.origin !== "http://{{bookmarklet_domain}}")
    				return;
				$("#trayframe_veil").fadeOut(750);
				$("#trayframe iframe").slideUp(500);
				setTimeout("$('#trayframe').remove()", 750);
			}
			window.addEventListener("message", receiveMessage, false);
		})();
	}

})();