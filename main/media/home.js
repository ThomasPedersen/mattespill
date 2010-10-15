$(function() {
	$('.restricted_room_msg').parent().hover(function() {
		$(this).find('.restricted_room_msg').fadeIn(300);
	}, function() {
		$(this).find('.restricted_room_msg').fadeOut(300);
	});
});