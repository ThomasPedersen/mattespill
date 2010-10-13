$(function() {
	$('.simple_button').click(function() {
		$.ajax({
			type: 'POST',
			url: '/answer/',
			dataType: 'json',
			data: {answer: $('input[name=answer]').val()},
			success: function(data, textStatus) {
				if (data.done) {
					document.location.href = '/room/'; // FIXME
				}
				else {
					$('#question_index').text(data.next_index);
					$('#question_text').text(data.next_question);
					
					if (data.correct) {
						$('#wrong_answer').hide();
						$('#correct_answer').fadeIn();
					}
					else {
						$('#correct_answer').hide();
						$('#wrong_answer').fadeIn();
					}
				}
			},
			error: function(XMLHttpRequest, textStatus) {
				alert('Det oppstod en feil');
			}
		});
	});
})