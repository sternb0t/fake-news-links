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

$(document).ready(function(){

    function getAttributes() {
        $.get("/api/attributes/")
            .done(function(data){
                var left = $('#contribute-attributes-left');
                var right = $('#contribute-attributes-right');

                for (var i = 0; i < data.results.length; i++) {
                   var attr = data.results[i];
                   var content = '<div class="form-check"><label class="form-check-label"><input class="contribute-attribute form-check-input" type="checkbox" value="' + attr.id + '"> ' + attr.name + '</label></div>';
                   if (i < data.results.length / 2) {
                       left.append(content);
                   }
                   else {
                       right.append(content);
                   }
                }
            })
            .fail(function(err){
                console.log(err);
            });
    }
    getAttributes();

    // get stats from api
    function getStats() {
        $.get("/api/stats/")
            .done(function(data){
                $('#fake-news-links-count').text(data.count);
            })
            .fail(function(err){
                console.log(err);
            });
    }
    getStats();

    // show recent data in the explore table
    $.fn.dataTable.moment("YYYY-MM-DDTHH:mm:ss.SSSSZ");
    var table = $('#fake-news-table').DataTable({
    ajax: {
        url: "/api/links/",
        dataSrc: "results"
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

    // refresh data with the refresh button
    $('#refresh-table').click(function(){
      table.ajax.reload();
      getStats();
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
            var contributeAttributes = ($('input.contribute-attribute:checkbox:checked')).map(function() {
                return {id: this.value};
            }).get();
            var data = {
                url: url,
                latitude: latitude,
                longitude: longitude,
                geo_accuracy: geoAccuracy,
                attributes: contributeAttributes
            };
            $.ajax({
              type: "POST",
              url: "/api/links/",
              data: JSON.stringify(data),
              contentType: "application/json",
              dataType: "json"
            }).done(function(){
                $('#contribute-url').val('');
                table.ajax.reload();
                getStats();
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
});

