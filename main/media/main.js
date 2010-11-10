var soundListener = new Object();

soundListener.onInit = function() {};
soundListener.onUpdate = function() {};

function getWindowWidth() {
	if (window.innerWidth)
		return window.innerWidth;
	else if (document.body.clientWidth)
		return document.body.clientWidth;
	else
		return 800;
}
function getWindowHeight() {
	if (window.innerHeight)
		return window.innerHeight;
	else if (document.body.clientHeight)
		return document.body.clientHeight;
	else
		return 600;
}

function updateFontSize() {
	$('body').css('font-size', getWindowWidth()/65 + 'px');
	//$('body').css('font-size', getWindowHeight()/40 + 'px');
}

$(window).resize(updateFontSize);
$(updateFontSize);


function playSound(name) {
	object = $('#audio_flash').get(0);

	object.SetVariable('method:setUrl', '/media/sounds/' + name);
	object.SetVariable('method:play', '');
	object.SetVariable('enabled', 'true');
}