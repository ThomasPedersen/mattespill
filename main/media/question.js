var bearTimer;
var expireTimer;


function nl2br(str) {
	return (str + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1' + '<br />' + '$2');
}

function showBear() {
	$('#hintbear img, #hintbear .dialogbox').css('cursor', 'pointer').click(function() {
		$.ajax({
			type: 'POST',
			url: '/buyhint/',
			dataType: 'json',
			complete: function() {
				$('#hintbear img, #hintbear .dialogbox').unbind('click').css('cursor', 'auto');
			},
			success: function(data, textStatus) {
				$('#num_points').text(data.points);

				if (data.hint == null) {
					$('#hintbear .dialogbox').text('Du har nok for lite gullmynter!');
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

	$('#hintbear .dialogbox').html('Har du lyst p&aring; hjelp?<br />Klikk p&aring; meg!<br />(Et hint koster 20 gullmynter)');
	$('#hintbear').show().animate({
		opacity: 1,
		marginRight: '-4em'
	}, 1000, function() {
		$('#hintbear .dialogbox').fadeIn(500);
	});

	playSound('slide_whistle_up.mp3');
}
function startBear() {
	bearTimer = setTimeout(showBear, 10000);
}
function stopBear() {
	if (bearTimer != null)
		clearTimeout(bearTimer);

	if ($('#hintbear').is(':visible')) {
		$('#hintbear').animate({
			opacity: 0,
			marginRight: '-7em'
		}, 400, $('#hintbear').hide);

		//playSound('slide_whistle_down.mp3');
	}
}

function resetExpire() {
	if (expireTimer != null)
		clearTimeout(expireTimer);

	expireTimer = setTimeout(function() {
		window.location = '/';
	}, 10000);
}


$(function() {
	$('.start_button').click(function() {
		if (!$('input[name=answer]').val().match(/^-?\d+$/)) {
			$('#correct_answer').hide();
			$('#wrong_answer').hide();
			$('#invalid_answer').fadeIn();	
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
					$('#earned_points').text(data.earned)
					$('#invalid_answer').hide();
					$('#wrong_answer').hide();
					$('#correct_answer').fadeIn();
					playSound('coins.mp3');
				}
				else {
					$('#lost_points').text(data.lost)
					$('#invalid_answer').hide();
					$('#correct_answer').hide();
					$('#wrong_answer').fadeIn();
					playSound('wrong.mp3');
				}

				// If turn finished
				if (data.index < 0) {
					$('#question_wrapper').remove();
					$('#finished_wrapper').show();
					playSound('applause.mp3');
				}
				else {
					$('input[name=answer]').val('').focus();
					$('#question_index').text(data.index);
					$('#question_text').text(data.question);

					startBear();
					//resetExpire();
				}
			},
			error: function(XMLHttpRequest, textStatus) {
				alert('Det oppstod en feil!');
			}
		});
	});

	var submit = function() {
		$('.simple_button').click();
		return false;
	};

	$('#answer_form').submit(submit);

	// IE HACK
	$('#answer_form input').keydown(function(e) {
		if (e.keyCode == 13) {
			$(this).parents('form').submit();
			return false;
		}
	});

	$('input[name=answer]').focus();
	startBear();
	//resetExpire();
});
