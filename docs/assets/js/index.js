var countDownDate = new Date("Jun 1, 2021 00:00:00").getTime();

$(function() {
    // Countdown timer
	// Various spans
	$(window).on('load', startCountdown);

	// Load random video
	loadRandomVideo();

    // Adjust gradient heights so that gradient always
    // matches the height of the trailer video
	adjustGradientHeight();
	$(window).on('resize', adjustGradientHeight);
})

function startCountdown () {
	var root = document.querySelector("#header .contents .countdown");

	var countdown = function() {
		root.innerHTML = "Available Now";
		return;

		// Get today's date and time
		var now = new Date().getTime();

		// Find the distance between now and the count down date
		var distance = countDownDate - now;

		// Time calculations for days, hours, minutes and seconds
		var months = Math.floor(distance / (1000 * 60 * 60 * 24 * 31));
		var days = Math.floor((distance % (1000 * 60 * 60 * 24 * 31)) / (1000 * 60 * 60 * 24));
		var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
		var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
		var seconds = Math.floor((distance % (1000 * 60)) / 1000);

		// Display the result in the various spans
		var showMonths = months != 0;
		var showDays = showMonths || days != 0;
		var showHours = showDays || hours != 0;
		var showMinutes = showHours || minutes != 0;
		var showSeconds = showMinutes || seconds != 0;
		root.innerHTML = `${(showMonths ? months + "mo" : '')} ${(showDays ? days + "d" : '')} ${(showHours ? hours + "h" : '')} ${(showMinutes ? minutes + "m" : '')} ${(showSeconds ? seconds + "s" : '')}`;
	};

	setInterval(countdown, 1000);
}

function loadRandomVideo () {
	var videoElement = document.querySelector("#header .vid video");
	var root = videoElement.getAttribute("video-src") + "\\";
	var videos = ["00.webm", "01.webm", "02.webm", "03.webm", "04.webm"];
	var posters = ["00.png", "01.png", "02.png", "03.png", "04.png"];

	var randomIndex = Math.floor(Math.random() * Math.min(videos.length, posters.length));
	videoElement.src = root + videos[randomIndex];
	videoElement.poster = root + posters[randomIndex];
}

function adjustGradientHeight () {
	// Adjust the height of the gradient to match with the height of the youtube video trailer
	var trailer = document.querySelector(".trailercontainer .trailer");
	var height = getOffsetTop(trailer) + trailer.getBoundingClientRect().height * .75;
	document.body.style.backgroundImage = `linear-gradient(186deg, #21cce2 0%, #21cce2 ${height}px, #ffffff ${height}px)`;
}

function getOffsetTop (element) {
	var distance = 0;
	do {
		// Increase our distance counter
		distance += element.offsetTop;
	
		// Set the element to it's parent
		element = element.offsetParent;
	
	} while (element);
	return distance < 0 ? 0 : distance;
}
