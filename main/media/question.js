var bearTimer;


function nl2br(str) {
	return (str + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1' + '<br />' + '$2');
}

function showBear() {
	$('#hintbear').css('cursor', 'pointer').click(function() {
		$.ajax({
			type: 'POST',
			url: '/buyhint/',
			dataType: 'json',
			complete: function() {
				$('#hintbear').unbind('click').css('cursor', 'auto');
			},
			success: function(data, textStatus) {
				$('#num_points').text(data.points);

				if (data.hint == null) {
					$('#hintbear .dialogbox').text('Du har nok for lite penger!');
					setTimeout(stopBear, 2000);
				}
				else
					$('#hintbear .dialogbox').html(nl2br(data.hint));
			},
			error: function(XMLHttpRequest, textStatus) {
				$('#hintbear .dialogbox').text('Det oppstod en feil');
				setTimeout(stopBear, 2000);
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
		if ($.trim($('input[name=answer]').val()) == '') {
			alert('Du må skrive inn noe!');
			$('input[name=answer]').val('');
			return;
		}

		stopBear();

		$.ajax({
			type: 'POST',
			url: '/answer/',
			dataType: 'json',
			data: {answer: $('input[name=answer]').val()},
			success: function(data, textStatus) {
				if (data.points <= 0) {
					window.location = '/game_over/';
					return;
				}

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
				alert('Det oppstod en feil!');
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