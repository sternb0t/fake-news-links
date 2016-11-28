/*!
 * Start Bootstrap - Grayscale Bootstrap Theme (http://startbootstrap.com)
 * Code licensed under the Apache License v2.0.
 * For details, see http://www.apache.org/licenses/LICENSE-2.0.
 */

// jQuery to collapse the navbar on scroll
function collapseNavbar() {
    if ($(".navbar").offset().top > 50) {
        $(".navbar-fixed-top").addClass("top-nav-collapse");
    } else {
        $(".navbar-fixed-top").removeClass("top-nav-collapse");
    }
}

$(window).scroll(collapseNavbar);
$(document).ready(collapseNavbar);

// jQuery for page scrolling feature - requires jQuery Easing plugin
$(function() {
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
});

// Closes the Responsive Menu on Menu Item Click
$('.navbar-collapse ul li a').click(function() {
    $(this).closest('.collapse').collapse('toggle');
});

// contribute a URL via the API
$('#contribute-form').submit(function(event) {
    event.preventDefault();
    $('.contribute-results').hide();
    $('#contribute-spinner').show();

    function doPost(position) {
        var url = $('#contribute-url').val();
        var latitude = position.coords && position.coords.latitude ? Math.round(position.coords.latitude * 100000) / 100000 : null;
        var longitude = position.coords && position.coords.longitude ? Math.round(position.coords.longitude * 100000) / 100000 : null;
        var geoAccuracy = position.coords && position.coords.accuracy ? Math.round(position.coords.accuracy * 100000) / 100000 : null;
        var data = {
            url: url,
            latitude: latitude,
            longitude: longitude,
            geo_accuracy: geoAccuracy
        };
        $.post("/api/links/", data)
            .done(function(){
                $('#contribute-spinner').hide();
                $('#contribute-success').show();
            })
            .fail(function(err){
                console.log(err);
                $('#contribute-spinner').hide();
                $('#contribute-fail').show();
            });
    }

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(doPost, doPost);
    }
    else {
        doPost();
    }

});

// get stats from api
$(document).ready(function(){
   $.get("/api/stats/")
       .done(function(data){
           $('#fake-news-links-count').text(data.count);
       })
       .fail(function(err){
           console.log(err);
       });

   $.fn.dataTable.moment("YYYY-MM-DDTHH:mm:ss.SSSSZ");
   $('#fake-news-table').DataTable({
    ajax: {
        url: "/api/links/",
        dataSrc: ""
    },
    columns: [
        {
            data: "url",
            render: function(data){
                return '<a href="' + data + '">' + data + '</a>';
            }
        },
        {
            data: "created_date",
            render: function(data){
                return moment(data).fromNow();
            }
        },
        {
            data: "created_date"
        }
    ],
    columnDefs: [
        {
            targets: [1],
            orderData:[2]
        },
        {
            targets: [2],
            visible: false,
            searchable: false
        }
    ],
    order: [[ 1, "desc" ]]
    });
});

