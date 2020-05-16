/*
	Visualize by TEMPLATED
	templated.co @templatedco
	Released for free under the Creative Commons Attribution 3.0 license (templated.co/license)
*/

var countDownDate = new Date("Jun 1, 2020 00:00:00").getTime();

$(function() {

	// Vars.
		var	$window = $(window),
			$body = $('body'),
			$wrapper = $('#wrapper');

	// Breakpoints.
		skel.breakpoints({
			xlarge:	'(max-width: 1680px)',
			large:	'(max-width: 1280px)',
			medium:	'(max-width: 980px)',
			small:	'(max-width: 736px)',
			xsmall:	'(max-width: 480px)'
		});

	// Disable animations/transitions until everything's loaded.
		$body.addClass('is-loading');

		$window.on('load', function() {
			$body.removeClass('is-loading');
		});

	// Poptrox.
		$window.on('load', function() {

			$('.thumbs').poptrox({
				onPopupClose: function() { $body.removeClass('is-covered'); },
				onPopupOpen: function() { $body.addClass('is-covered'); },
				baseZIndex: 10001,
				useBodyOverflow: false,
				usePopupEasyClose: true,
				overlayColor: '#000000',
				overlayOpacity: 0.75,
				popupLoaderText: '',
				fadeSpeed: 500,
				usePopupDefaultStyling: false,
				windowMargin: (skel.breakpoint('small').active ? 5 : 50)
			});

		});

	// Countdown timer
	// Various spans
	$window.on('load', startCountdown);

	// Load random video
	loadRandomVideo();

});

function startCountdown () {
	var root = document.querySelector("#header .contents .countdown");
	var eDays = root.querySelector('.days');
	var eHours = root.querySelector('.hours');
	var eMinutes = root.querySelector('.minutes');
	var eSeconds = root.querySelector('.seconds');

	var countdown = function() {
		// Get today's date and time
		var now = new Date().getTime();

		// Find the distance between now and the count down date
		var distance = countDownDate - now;

		// Time calculations for days, hours, minutes and seconds
		var days = Math.floor(distance / (1000 * 60 * 60 * 24));
		var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
		var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
		var seconds = Math.floor((distance % (1000 * 60)) / 1000);

		// Display the result in the various spans
		eDays.innerHTML = days;
		eHours.innerHTML = hours;
		eMinutes.innerHTML = minutes;
		eSeconds.innerHTML = seconds;
	};

	setInterval(countdown, 1000);
}

function loadRandomVideo () {
	var root = "videos/levels/";
	var videos = ["00.webm", "01.webm", "02.webm", "03.webm", "04.webm"];
	var posters = ["00.png", "01.png", "02.png", "03.png", "04.png"];

	var videoElement = document.querySelector("#header .vid video");
	var randomIndex = Math.floor(Math.random() * Math.min(videos.length, posters.length));
	videoElement.src = root + videos[randomIndex];
	videoElement.poster = root + posters[randomIndex];
}
