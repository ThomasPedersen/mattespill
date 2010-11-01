var peekbearImages = ['peekbearbottom.png', 'peekbearright.png', 'peekbearleft.png'];

function showPeekbear() {
	var i = Math.floor(Math.random()*(peekbearImages.length+1));
	var element = $('<img src="/media/images/' + peekbearImages[i] + '" alt="Tittei" />').
		css('position', 'fixed');

	switch (i) {
		case 0:
			element.css('height', '5em').css('bottom', '-5em').
			css('left', Math.floor(5 + Math.random()*(80-5)) + '%').animate({
				bottom: '0em'
			}, 2000, function() {
				$(this).animate({
					bottom: '-5em'
				}, 300, function() {
					$('body').remove(this);
				});
			});
			break;
		case 1:
			element.css('width', '5em').css('right', '-5em').
			css('top', Math.floor(5 + Math.random()*(80-5)) + '%').animate({
				right: '0em'
			}, 2000, function() {
				$(this).animate({
					right: '-5em'
				}, 300, function() {
					$('body').remove(this);
				});
			});
			break;
		case 2:
			element.css('width', '5em').css('left', '-5em').
			css('top', Math.floor(5 + Math.random()*(80-5)) + '%').animate({
				left: '0em'
			}, 2000, function() {
				$(this).animate({
					left: '-5em'
				}, 300, function() {
					$('body').remove(this);
				});
			});
			break;
	}

	$('body').append(element);
}

$(function() {
	setInterval(showPeekbear, 3000);
	showPeekbear();
});
