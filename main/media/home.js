$(function() {
	$('.restricted_room_msg').parent().hover(function() {
		$(this).find('.restricted_room_msg').fadeIn(100);
	}, function() {
		$(this).find('.restricted_room_msg').fadeOut(300);
	});

	$('#treasure_chest').css('cursor', 'pointer').click(function() {
		playSound('coins2.mp3');
	});
});