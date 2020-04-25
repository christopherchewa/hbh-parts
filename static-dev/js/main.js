var WOW;
$(function () {

    // Material select
    $('.mdb-select').materialSelect();

    $(".quickView").click(function (e) {
        e.preventDefault();
    });

    // Scroll event
    $(window).scroll(function () {

        let aciveSec = $(".staticNav").find(".active");

        if (this.window.pageYOffset > 1300 && this.window.pageYOffset < 1600) {
            aciveSec.removeClass("active");
            $(".ph").addClass("active");
        } else if (this.window.pageYOffset > 1600 && this.window.pageYOffset < 1800) {
            aciveSec.removeClass("active");
            $(".c").addClass("active");
        } else if (this.window.pageYOffset > 1800) {
            aciveSec.removeClass("active");
            $(".p").addClass("active");
        } else if (this.window.pageYOffset < 1300) {
            aciveSec.removeClass("active");
            $(".g").addClass("active");
        }
    })

    // Login form toggle
    $(".nav-item.account").click(function () {
        $(".loginForm").fadeToggle();
    })


    // Mobile Menu
    $(".navbar-toggler").click(function () {
        $(".mobileMenuInner").addClass('mobileMenuInnerToggle');
        $('body').css({
            'overflow': 'hidden'
        });
    })

    $(".mobileMenuInner span").click(function () {
        $(".mobileMenuInner").removeClass('mobileMenuInnerToggle');
        $('body').css({
            'overflow': 'initial'
        });
    })

    // staticNav scroll
    var $sidebar = $(".staticNav"),
        $window = $(window),
        offset = $sidebar.offset(),
        topPadding = 15;

    $(window).scroll(function () {
        if ($window.scrollTop() > offset.top) {
            $sidebar.stop().animate({
                marginTop: $window.scrollTop() - offset.top + topPadding
            });
        } else {
            $sidebar.stop().animate({
                marginTop: 0
            });
        }
    })


   /* // innerListing slider *
    var sync1 = $("#sync1");
    var sync2 = $("#sync2");

    sync1.owlCarousel({
        items: 1,
        slideSpeed: 3000,
        nav: false,
        loop: false,
        dots: false,
        responsiveRefreshRate: 200,
    }).on("changed.owl.carousel", syncPosition);

    sync2.owlCarousel({
        items: 3,
        loop: false,
        dots: false,
        responsiveRefreshRate: 100,
    }).on("initialized.owl.carousel", function (el) {
        el.find(".owl-item").eq(0).addClass("synced");
    });

    function syncPosition(el) {
        var current = this.currentItem;
        sync2
            .find(".owl-item")
            .removeClass("synced")
            .eq(current)
            .addClass("synced")
        if ($("#sync2").data("owlCarousel") !== undefined) {
            center(current)
        }
    }

    $("#sync2").on("click", ".owl-item", function (e) {
        e.preventDefault();
        var number = $(this).index();
        sync1.data('owl.carousel').to(number, 300, true);
    });

    function center(number) {
        var sync2visible = sync2.data("owl.carousel").owl.visibleItems;
        var num = number;
        var found = false;
        for (var i in sync2visible) {
            if (num === sync2visible[i]) {
                var found = true;
            }
        }

        if (found === false) {
            if (num > sync2visible[sync2visible.length - 1]) {
                sync2.trigger("owl.goTo", num - sync2visible.length + 2)
                sync2.data('owl.carousel').to(num - sync2visible.length + 2, 300, true);
            } else {
                if (num - 1 === -1) {
                    num = 0;
                }
                sync2.data('owl.carousel').to(num, 300, true);
            }
        } else if (num === sync2visible[sync2visible.length - 1]) {
            sync2.data('owl.carousel').to(sync2visible[1], 300, true);
        } else if (num === sync2visible[0]) {
            sync2.data('owl.carousel').to(num - 1, 300, true);
        }
    }

})*/

//Preloader

$(window).on('load', function () { // makes sure the whole site is loaded 
    $('#status').fadeOut(); // will first fade out the loading animation 
    $('#preloader').delay(350).fadeOut('slow'); // will fade out the white DIV that covers the website. 
    $('body').delay(350).css({
        'overflow': 'visible'
    });
})