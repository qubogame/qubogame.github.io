/*
	Visualize by TEMPLATED
	templated.co @templatedco
	Released for free under the Creative Commons Attribution 3.0 license (templated.co/license)
*/

$(function() {
	// Breakpoints.
		skel.breakpoints({
			xlarge:	'(max-width: 1680px)',
			large:	'(max-width: 1280px)',
			medium:	'(max-width: 980px)',
			small:	'(max-width: 736px)',
			xsmall:	'(max-width: 480px)'
		});

	// Disable animations/transitions until everything's loaded.
	$("body").addClass('is-loading');

	$(window).on('load', function() {
		$("body").removeClass('is-loading');
	});

	// Poptrox.
	$(window).on('load', function() {

		$('.thumbs').poptrox({
			onPopupClose: function() { $("body").removeClass('is-covered'); },
			onPopupOpen: function() { $("body").addClass('is-covered'); },
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

	$('#footer-view').load("assets/views/footer.html", function () {
		// Disclaimer modal
		showModal(document.querySelector("#disclaimer-button"),
			document.querySelector("#disclaimer-modal"));
	});
});

function showModal (button, modal) {
	var onopen = function () {
		modal.classList.add("display");
	}
	var onclose = function () {
		modal.classList.remove("display");
	}

	var close = modal.querySelector(".close");

	button.onclick = onopen;
	close.onclick = onclose;
	window.addEventListener("click", function(event) {
		if (event.target == modal) {
			onclose();
		}
	});
}
