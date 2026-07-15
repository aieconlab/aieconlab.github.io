// Passive event listeners
jQuery.event.special.touchstart = {
	setup: function (_, ns, handle) {
		this.addEventListener("touchstart", handle, {
			passive: !ns.includes("noPreventDefault")
		});
	}
};
jQuery.event.special.touchmove = {
	setup: function (_, ns, handle) {
		this.addEventListener("touchmove", handle, {
			passive: !ns.includes("noPreventDefault")
		});
	}
};

// Preloader js
function preloader() {
	$('.preloader').delay(100).fadeOut(10);
}
$(preloader);
$(document).on("turbolinks:load", preloader);

(function ($) {
	'use strict';


	//  Search Form Open
	var $searchOpen = $('#searchOpen');
	var $searchClose = $('#searchClose');
	var $searchWrapper = $('#site-search-wrapper');

	function openSearch() {
		$searchWrapper.addClass('open').attr('aria-hidden', 'false');
		$searchOpen.attr('aria-expanded', 'true');
		setTimeout(function () {
			$('#site-search-query').trigger('focus');
		}, 400);
	}

	function closeSearch() {
		$searchWrapper.removeClass('open').attr('aria-hidden', 'true');
		$searchOpen.attr('aria-expanded', 'false').trigger('focus');
	}

	$searchOpen.on('click', openSearch);
	$searchClose.on('click', closeSearch);
	$(document).on('keydown', function (event) {
		if (event.key === 'Escape' && $searchWrapper.hasClass('open')) {
			closeSearch();
		}
	});


	// tab
	$('.tab-content').find('.tab-pane').each(function (idx, item) {
		var navTabs = $(this).closest('.code-tabs').find('.nav-tabs'),
			title = $(this).attr('title');
		navTabs.append('<li class="nav-item"><a class="nav-link" href="#">' + title + '</a></li>');
	});

	$('.code-tabs ul.nav-tabs').each(function () {
		$(this).find("li:first").addClass('active');
	})

	$('.code-tabs .tab-content').each(function () {
		$(this).find("div:first").addClass('active');
	});

	$('.nav-tabs a').click(function (e) {
		e.preventDefault();
		var tab = $(this).parent(),
			tabIndex = tab.index(),
			tabPanel = $(this).closest('.code-tabs'),
			tabPane = tabPanel.find('.tab-pane').eq(tabIndex);
		tabPanel.find('.active').removeClass('active');
		tab.addClass('active');
		tabPane.addClass('active');
	});


	// Accordions
	$('.collapse').on('shown.bs.collapse', function () {
		$(this).parent().find('.fas fa-plus').removeClass('fas fa-plus').addClass('fas fa-minus');
	}).on('hidden.bs.collapse', function () {
		$(this).parent().find('.fas fa-minus').removeClass('fas fa-minus').addClass('fas fa-plus');
	});



	//easeInOutExpo Declaration
	jQuery.extend(jQuery.easing, {
		easeInOutExpo: function (x, t, b, c, d) {
			if (t == 0) return b;
			if (t == d) return b + c;
			if ((t /= d / 2) < 1) return c / 2 * Math.pow(2, 10 * (t - 1)) + b;
			return c / 2 * (-Math.pow(2, -10 * --t) + 2) + b;
		}
	});

	// back to top button
	$('#scrollTop').click(function (e) {
		e.preventDefault();
		$('html,body').animate({
			scrollTop: 0
		}, 1500, "easeInOutExpo");
	});

	// Slider code is safe on pages where the conditional Slick bundle is absent.
	if ($.fn.slick) {
		if ($('.post-slider').length) {
			$('.post-slider').slick({
				slidesToShow: 1,
				slidesToScroll: 1,
				autoplay: true,
				dots: false,
				arrows: true,
				prevArrow: '<button type=\'button\' class=\'prevArrow\' aria-label=\'이전 이미지\'><i class=\'fas fa-angle-left\' aria-hidden=\'true\'></i></button>',
				nextArrow: '<button type=\'button\' class=\'nextArrow\' aria-label=\'다음 이미지\'><i class=\'fas fa-angle-right\' aria-hidden=\'true\'></i></button>'
			});
		}

		if ($('.featured-post-slider').length) {
			$('.featured-post-slider').slick({
				slidesToShow: 1,
				slidesToScroll: 1,
				autoplay: true,
				dots: true,
				arrows: true,
				vertical: false,
				prevArrow: '<button type=\'button\' class=\'prevArrow\' aria-label=\'이전 글\'><i class=\'fas fa-angle-left\' aria-hidden=\'true\'></i></button>',
				nextArrow: '<button type=\'button\' class=\'nextArrow\' aria-label=\'다음 글\'><i class=\'fas fa-angle-right\' aria-hidden=\'true\'></i></button>'
			});
		}

		if ($('.single-product-slider').length) {
			$('.single-product-slider').slick({
				autoplay: false,
				infinite: true,
				arrows: false,
				dots: true,
				customPaging: function (slider, i) {
					var image = $(slider.$slides[i]).data('image');
					return '<img class="img-fluid" src="' + image + '" alt="product-img">';
				}
			});
		}
	}

})(jQuery);
