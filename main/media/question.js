var bearTimer;

function showBear() {
	$('#hintbear').css('cursor', 'pointer').click(function() {
		$.ajax({
			type: 'POST',
			url: '/buyhint/',
			dataType: 'json',
			success: function(data, textStatus) {
				$('#hintbear').unbind('click').css('cursor', 'auto');

				if (data.hint == null) {
					$('#hintbear .dialogbox').text(data.hint);
					return;
				}

				$('#hintbear .dialogbox').text(data.hint);

				$('#num_points').text(data.points);
			},
			error: function(XMLHttpRequest, textStatus) {
				alert('Det oppstod en feil');
			}
		});
	});

	$('#hintbear .dialogbox').html('Har du lyst p&aring; hjelp?<br />Klikk p&aring; meg!');
	$('#hintbear').show().animate({
		opacity: 1,
		marginRight: '0em'
	}, 1000, function() {
		$('#hintbear .dialogbox').fadeIn(500);
	});
}
function startBear() {
	bearTimer = setTimeout(showBear, 5000);
}
function stopBear() {
	if (bearTimer != null)
		clearTimeout(bearTimer);

	$('#hintbear').animate({
		opacity: 0,
		marginRight: '-7em'
	}, 400, $('#hintbear').hide);
}

$(function() {
	$('.start_button').click(function() {
		stopBear();

		if ($.trim($('input[name=answer]').val()) == '') {
			alert('Du må skrive inn noe!');
			$('input[name=answer]').val('');
			return;
		}

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

					startBear();
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
});