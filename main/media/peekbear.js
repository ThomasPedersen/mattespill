var peekbearImages = ['peekbearbottom.png', 'peekbearright.png', 'peekbearleft.png'];

function showPeekbear() {
	var i = Math.floor(Math.random()*(peekbearImages.length));
	var element = $('<img id="peekbear" src="/media/images/' + peekbearImages[i] + '" alt="Tittei" />').
		css('position', 'fixed');

	var bearSize = '3em';

	switch (i) {
		case 0:
			element.css('height', bearSize).css('bottom', '-' + bearSize).
			css('left', Math.floor(5 + Math.random()*(80-5)) + '%').animate({
				bottom: '0em'
			}, 2000, function() {
				$(this).animate({
					bottom: '-' + bearSize
				}, 300, function() {
					$(this).remove();
				});
			});
			break;
		case 1:
			element.css('width', bearSize).css('right', '-' + bearSize).
			css('bottom', Math.floor(5 + Math.random()*(80-5)) + '%').animate({
				right: '0em'
			}, 2000, function() {
				$(this).animate({
					right: '-' + bearSize
				}, 300, function() {
					$(this).remove();
				});
			});
			break;
		case 2:
			element.css('width', bearSize).css('left', '-' + bearSize).
			css('bottom', Math.floor(5 + Math.random()*(80-5)) + '%').animate({
				left: '0em'
			}, 2000, function() {
				$(this).animate({
					left: '-' + bearSize
				}, 300, function() {
					$(this).remove();
				});
			});
			break;
		default:
			return;
	}

	$('body').append(element);
	$('#peekbear').css('cursor', 'pointer').click(function() {
		playSound('slide_whistle_up.mp3');
	});
}

$(function() {
	setInterval(showPeekbear, 15000);
	showPeekbear();
});
