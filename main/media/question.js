$(function() {
	$('.simple_button').click(function() {
		alert($('input[name=answer]').val());
		$.ajax({
			type: 'POST',
			url: '/answer/',
			dataType: 'json',
			data: {answer: $('input[name=answer]').val()},
			success: function(data, textStatus) {
				alert(data);
			},
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				alert(textStatus + ' : ' + errorThrown);
			}
		});
	});
})