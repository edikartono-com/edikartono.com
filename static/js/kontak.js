/**
* Template Name: DevFolio - v2.3.0
* Template URL: https://bootstrapmade.com/devfolio-bootstrap-portfolio-html-template/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/
(function($) {
    "use strict";
  
    var nav = $('nav');
  
    $('.navbar-toggler').on('click', function() {
      if (!$('#mainNav').hasClass('navbar-reduce')) {
        $('#mainNav').addClass('navbar-reduce');
      }
    })
  
    // Preloader
    $(window).on('load', function() {
      if ($('#preloader').length) {
        $('#preloader').delay(100).fadeOut('slow', function() {
          $(this).remove();
        });
      }
    });
  
    // Back to top button
    $(window).scroll(function() {
      if ($(this).scrollTop() > 100) {
        $('.back-to-top').fadeIn('slow');
      } else {
        $('.back-to-top').fadeOut('slow');
      }
    });
    
    $('.back-to-top').click(function() {
      $('html, body').animate({
        scrollTop: 0
      }, 1500, 'easeInOutExpo');
      return false;
    });
  
    /*--/ Star ScrollTop /--*/
    $('.scrolltop-mf').on("click", function() {
      $('html, body').animate({
        scrollTop: 0
      }, 1000);
    });
    
  })(jQuery);