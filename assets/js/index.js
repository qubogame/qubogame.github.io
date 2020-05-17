var countDownDate = new Date("Jun 1, 2020 00:00:00").getTime();

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

function adjustGradientHeight () {
	// Adjust the height of the gradient to match with the height of the youtube video trailer
	var trailer = document.querySelector(".trailercontainer .trailer");
	var height = getOffsetTop(trailer) + trailer.getBoundingClientRect().height * .75;
	document.body.style.backgroundImage = `linear-gradient(186deg, #21cce2 0%, #21cce2 ${height-75}px, #ffffff ${height+75}px)`;
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