type = ['','info','success','warning','danger'];

function getMonthBased (monthBased) {
  var last_max = 0
  var last_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  for (var x=1; x <= last_values.length; x++) {
    if (monthBased[x] != null) {
      if (monthBased[x] > last_max) {last_max = monthBased[x]}
      last_values[x-1] = monthBased[x]
    }
  }
  return [last_values,last_max]
}

demo = {
    initPickColor: function(){
        $('.pick-class-label').click(function(){
            var new_class = $(this).attr('new-class');
            var old_class = $('#display-buttons').attr('data-class');
            var display_div = $('#display-buttons');
            if(display_div.length) {
            var display_buttons = display_div.find('.btn');
            display_buttons.removeClass(old_class);
            display_buttons.addClass(new_class);
            display_div.attr('data-class', new_class);
            }
        });
    },

    checkScrollForTransparentNavbar: debounce(function() {
            $navbar = $('.navbar[color-on-scroll]');
            scroll_distance = $navbar.attr('color-on-scroll') || 500;

            if($(document).scrollTop() > scroll_distance ) {
                if(transparent) {
                    transparent = false;
                    $('.navbar[color-on-scroll]').removeClass('navbar-transparent');
                    $('.navbar[color-on-scroll]').addClass('navbar-default');
                }
            } else {
                if( !transparent ) {
                    transparent = true;
                    $('.navbar[color-on-scroll]').addClass('navbar-transparent');
                    $('.navbar[color-on-scroll]').removeClass('navbar-default');
                }
            }
    }, 17),

    initDocChartist: function(){
        var dataSales = {
          labels: ['9:00AM', '12:00AM', '3:00PM', '6:00PM', '9:00PM', '12:00PM', '3:00AM', '6:00AM'],
          series: [
             [287, 385, 490, 492, 554, 586, 698, 695, 752, 788, 846, 944],
            [67, 152, 143, 240, 287, 335, 435, 437, 539, 542, 544, 647],
            [23, 113, 67, 108, 190, 239, 307, 308, 439, 410, 410, 509]
          ]
        };

        var optionsSales = {
          lineSmooth: false,
          low: 0,
          high: 800,
          showArea: true,
          height: "245px",
          axisX: {
            showGrid: false,
          },
          lineSmooth: Chartist.Interpolation.simple({
            divisor: 3
          }),
          showLine: false,
          showPoint: false,
        };

        var responsiveSales = [
          ['screen and (max-width: 640px)', {
            axisX: {
              labelInterpolationFnc: function (value) {
                return value[0];
              }
            }
          }]
        ];

        Chartist.Line('#chartHours', dataSales, optionsSales, responsiveSales);


        var data = {
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          series: [
            [542, 443, 320, 780, 553, 453, 326, 434, 568, 610, 756, 895],
            [412, 243, 280, 580, 453, 353, 300, 364, 368, 410, 636, 695]
          ]
        };

        var options = {
            seriesBarDistance: 10,
            axisX: {
                showGrid: false
            },
            height: "245px"
        };

        var responsiveOptions = [
          ['screen and (max-width: 640px)', {
            seriesBarDistance: 5,
            axisX: {
              labelInterpolationFnc: function (value) {
                return value[0];
              }
            }
          }]
        ];

        Chartist.Bar('#chartActivity', data, options, responsiveOptions);

        var dataPreferences = {
            series: [
                [25, 30, 20, 25]
            ]
        };

        var optionsPreferences = {
            donut: true,
            donutWidth: 40,
            startAngle: 0,
            total: 100,
            showLabel: false,
            axisX: {
                showGrid: false
            }
        };

        Chartist.Pie('#chartPreferences', dataPreferences, optionsPreferences);

        Chartist.Pie('#chartPreferences', {
          labels: ['62%','32%','6%'],
          series: [62, 32, 6]
        });
    },

    initChartist: function(){
        // Type based:
        var last_str = document.getElementById('last_json').value;
        var last_json = JSON.parse(last_str);
        var typeBased = last_json['typeBased']['amount'];
        var monthBased = last_json['monthBased']['amount'];
        
        var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        var arr = getMonthBased(monthBased)
        var last_max = arr.pop()
        var last_values = arr.pop()

        // Last Report based on Type
        var last_type_keys = []
        var last_type_values = []
        var count = 1
        var html_typeBased = ''
        for (var x in typeBased) {
          last_type_keys.push(typeBased[x])
          last_type_values.push(typeBased[x])
          html_typeBased += '<i class="point color'+count+'"></i> '+x+'  '
          count++
        }
        document.getElementById("last_report_labels").innerHTML = html_typeBased;

        Chartist.Pie('#lastReport_type', {
          labels: last_type_keys,
          series: last_type_values
        });

        // Last Report based on Month
        var last_data = {labels: months,series: [last_values]}
        var last_options = {
          lineSmooth: false,
          low: 0,
          high: last_max,
          showArea: true,
          height: "245px",
          axisX: {
            showGrid: false,
          },
          lineSmooth: Chartist.Interpolation.simple({
            divisor: 3
          }),
          showLine: false,
          showPoint: false,
        };

        var responsiveSales = [
          ['screen and (max-width: 640px)', {
            axisX: {
              labelInterpolationFnc: function (value) {
                return value[0];
              }
            }
          }]
        ];

        Chartist.Line('#lastReport_month', last_data, last_options, responsiveSales)


        // All Reports based on Type
        var allReportsType_labels = []
        var allReportsType_values = []
        var allReportsType_str = document.getElementById('reportsType_json').value;
        var allReportsType = JSON.parse(allReportsType_str)
        var allReportsType_html = ''
        count = 1
        for (type in allReportsType) {
          allReportsType_labels.push(type)
          allReportsType_values.push(allReportsType[type])
          allReportsType_html += '<i class="point color'+count+'"></i> '+type+'  '
          count++
        }
        document.getElementById("AllReports_type_labels").innerHTML = allReportsType_html;

        Chartist.Pie('#allReports_type', {
          labels: allReportsType_values,
          series: allReportsType_values
        })



        // All Reports based on Month
                
        var all_str = document.getElementById('reports_json').value;
        var reports_json = JSON.parse(all_str);
        var allReports_values = []
        var all_max = 0
        for (key in reports_json) {
          var monthBased = reports_json[key]['monthBased']['amount'];
          var arr = getMonthBased(monthBased)
          var max = arr.pop()
          var values = arr.pop()
          allReports_values.push(values)
          if (max > all_max) {all_max = max}
        }

        var all_data = {labels: months,series: allReports_values}
        var all_options = {
          lineSmooth: false,
          low: 0,
          high: all_max,
          showArea: true,
          height: "245px",
          axisX: {
            showGrid: false,
          },
          lineSmooth: Chartist.Interpolation.simple({
            divisor: 3
          }),
          showLine: false,
          showPoint: false,
        };
        Chartist.Line('#allReports_month', all_data, all_options, responsiveSales)

        var reports_name_str = document.getElementById('reports_name').value;
        var reports_name = JSON.parse(reports_name_str);
        var count = 1
        var reportsNames_html = ''
        var reports_names = []
        for (id in reports_name) {
          reports_names.push(reports_name[id])
          reportsNames_html += '<i class="point color'+count+'"></i> '+reports_name[id]+'  '
          count++
        }
        document.getElementById("AllReports_month_labels").innerHTML = reportsNames_html;



        // All Reports Based On Year
        reports_year = []
        for (key in reports_json) {
          var values = []
          var typeBased = reports_json[key]['typeBased']['amount'];
          console.log('start')
          for (type in typeBased) {
            values.push(typeBased[type])
            console.log('type: '+type+', value: '+typeBased[type])
          }
          console.log('end')
          reports_year.push(values)
        }
        console.log(reports_year)


        var data = {
          labels: reports_names,
          series: [
            [3405,1751,2680],
            [422,942,1440],
            [480,340,740],
            [2243,1300,499]
          ]
        };

        var options = {
            seriesBarDistance: 10,
            axisX: {
                showGrid: false
            },
            height: "280px"
        };

        var responsiveOptions = [
          ['screen and (max-width: 640px)', {
            seriesBarDistance: 5,
            axisX: {
              labelInterpolationFnc: function (value) {
                return value[0];
              }
            }
          }]
        ];

        Chartist.Bar('#allReports_year', data, options, responsiveOptions);
        document.getElementById("AllReports_year_labels").innerHTML = allReportsType_html;
    },

    /*initGoogleMaps: function(){
        var myLatlng = new google.maps.LatLng(40.748817, -73.985428);
        var mapOptions = {
          zoom: 13,
          center: myLatlng,
          scrollwheel: false, //we disable de scroll over the map, it is a really annoing when you scroll through page
          styles: [{"featureType":"water","stylers":[{"saturation":43},{"lightness":-11},{"hue":"#0088ff"}]},{"featureType":"road","elementType":"geometry.fill","stylers":[{"hue":"#ff0000"},{"saturation":-100},{"lightness":99}]},{"featureType":"road","elementType":"geometry.stroke","stylers":[{"color":"#808080"},{"lightness":54}]},{"featureType":"landscape.man_made","elementType":"geometry.fill","stylers":[{"color":"#ece2d9"}]},{"featureType":"poi.park","elementType":"geometry.fill","stylers":[{"color":"#ccdca1"}]},{"featureType":"road","elementType":"labels.text.fill","stylers":[{"color":"#767676"}]},{"featureType":"road","elementType":"labels.text.stroke","stylers":[{"color":"#ffffff"}]},{"featureType":"poi","stylers":[{"visibility":"off"}]},{"featureType":"landscape.natural","elementType":"geometry.fill","stylers":[{"visibility":"on"},{"color":"#b8cb93"}]},{"featureType":"poi.park","stylers":[{"visibility":"on"}]},{"featureType":"poi.sports_complex","stylers":[{"visibility":"on"}]},{"featureType":"poi.medical","stylers":[{"visibility":"on"}]},{"featureType":"poi.business","stylers":[{"visibility":"simplified"}]}]

        }
        var map = new google.maps.Map(document.getElementById("map"), mapOptions);

        var marker = new google.maps.Marker({
            position: myLatlng,
            title:"Hello World!"
        });

        // To add the marker to the map, call setMap();
        marker.setMap(map);
    },*/

	showNotification: function(from, align){
    	color = Math.floor((Math.random() * 4) + 1);

    	$.notify({
        	icon: "pe-7s-gift",
        	message: "Welcome to <b>Light Bootstrap Dashboard</b> - a beautiful freebie for every web developer."

        },{
            type: type[color],
            timer: 4000,
            placement: {
                from: from,
                align: align
            }
        });
	}


}
