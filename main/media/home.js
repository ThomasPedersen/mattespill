$(function() {
	$('.restricted_room_msg').parent().hover(function() {
		$(this).find('.restricted_room_msg').fadeIn(100);
	}, function() {
		$(this).find('.restricted_room_msg').fadeOut(300);
	});
});