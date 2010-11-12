$(function() {
	$('.group .toggle').hide();
	$('.group h2').css('cursor', 'pointer').click(function() {
		$(this).siblings('.toggle').slideToggle();
	});
});