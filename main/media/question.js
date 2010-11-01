var bearTimer;

function showBear() {
	$('#hintbear').show().animate({
		opacity: 1,
		marginRight: '0em',
	}, 1000, function() {
		$('#hintbear .dialogbox').fadeIn(500);
	});
}
function startBear() {
	bearTimer = setTimeout(showBear, 1000);
}
function stopBear() {
	if (bearTimer != null)
		clearTimeout(bearTimer);
}

$(function() {
	$('.start_button').click(function() {
		if ($.trim($('input[name=answer]').val()) == '') {
			alert('Du må skrive inn noe!');
			$('input[name=answer]').val('');
			return;
		}

		startBear();

		$.ajax({
			type: 'POST',
			url: '/answer/',
			dataType: 'json',
			data: {answer: $('input[name=answer]').val()},
			success: function(data, textStatus) {
				$('#num_points').text(data.points);

				if (data.correct) {
					$('#wrong_answer').hide();
					$('#correct_answer').fadeIn();
				}
				else {
					$('#correct_answer').hide();
					$('#wrong_answer').fadeIn();
				}

				if (data.index < 0) {
					$('#question_wrapper').remove();
					$('#finished_wrapper').show();
				}
				else {
					$('input[name=answer]').val('').focus();
					$('#question_index').text(data.index);
					$('#question_text').text(data.question);
				}
			},
			error: function(XMLHttpRequest, textStatus) {
				alert('Det oppstod en feil');
			}
		});
	});

	$('#answer_form').submit(function() {
		$('.simple_button').click();
		return false;
	});

	$('input[name=answer]').focus();
	startBear();

	$('#hintbear').click(function() {
		alert('aaaaahh');
	});
});