// 01 - Basic Java Script

// jQuery to collapse the navbar on scroll
$(window).scroll(function() {
  if ($(".navbar").offset().top > 50) {
    $(".navbar-fixed-top").addClass("top-nav-collapse");
  } else {
    $(".navbar-fixed-top").removeClass("top-nav-collapse");
  }
});

// jQuery for page scrolling feature - requires jQuery Easing plugin

$(function() {
  $('.page-scroll a').bind('click', function(event) {
    var $anchor = $(this);
    $('html, body').stop().animate({
      scrollTop: $($anchor.attr('href')).offset().top
    }, 800, 'easeInOutExpo');
    event.preventDefault();
  });
});

// Rotate JS
var deg = 0;
window.setInterval(function() {
  deg += 1;
  $(".rotate").css('-webkit-transform','rotate(' + deg + 'deg)');
}, 25);


// 05 - Video Content BG Center Image

$(window).load(function() {
  centerContent();
});

$(window).resize(function() {
  centerContent();
});

function centerContent() {
  var container = $('.video-image');
  var content = $('.video-image img');
  content.css("left", (container.width()-content.width())/2);
  content.css("top", (container.height()-content.height())/2);
}

// 12 - Waypoints (Parallax)

$(".wp1").waypoint( function() { $(".wp1").addClass("animated fadeInDown"); }, { offset: "75%" });
$(".wp2").waypoint( function() { $(".wp2").addClass("animated fadeInUp"); }, { offset: "75%" });
