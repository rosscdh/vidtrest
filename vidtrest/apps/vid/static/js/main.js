/* 01 - Basic Java Script
-----------------------------------------------------------*/

// copy to Clipboard
new Clipboard("#copytoclipboard");


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


/* 05 - Video Content BG Center Image
-----------------------------------------------------------*/

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

/* 08 - Media Buttons
-----------------------------------------------------------*/

// Onclick Java Script

var player = document.getElementById('player');

$(".play-btn").on('click', function() {
   $(this).hide();
   $('.video-image').css('display', 'none');
   $('.video-container #player').css('display', 'inline-block');
   $(".pause-btn").show();
   $('.about-btn').css('display', 'none');
   $('.pause-btn').css('display', 'inline-block');
   $('.media-btns').css('margin-top', '440px');
   $('.intro-info-wrapper').css('display', 'none');
   $('.video-content .overlay').css('background', 'none');

   player.play();
});

$(".pause-btn").on('click', function() {
   $(this).hide();
   $(".play-btn").show();
   $('.video-container #player').hide();
   $('.video-image').css('display', 'block');
   $('.about-btn').css('display', 'inline-block');
   $('.play-btn').css('display', 'inline-block');
   $('.intro-info-wrapper').css('display', 'block');
   $('.media-btns').css('margin-top', '0px');
   $('.video-content .overlay').css('background', 'rgba(0,0,0,0.4) url(' + window.overlay_img_path + ')');
   $('.video-container #player').css('display', 'none');

   player.pause();
});

$(document).ready(function() {
  $(".play-btn").show();
  $('.video-container #player').hide();
  $('.video-image').css('display', 'block');
  $('.about-btn').css('display', 'inline-block');
  $('.play-btn').css('display', 'inline-block');
  $('.intro-info-wrapper').css('display', 'block');
  $('.media-btns').css('margin-top', '0px');
  $('.video-content .overlay').css('background', 'rgba(0,0,0,0.4) url(' + window.overlay_img_path + ')');
  $('.video-container #player').css('display', 'none');
});


/* 12 - Waypoints (Parallax)
-----------------------------------------------------------*/

$('.wp1').waypoint(function() {
$('.wp1').addClass('animated fadeInDown');
}, {
offset:'75%'
});
$('.wp2').waypoint(function() {
$('.wp2').addClass('animated fadeInUp');
}, {
offset:'75%'
});