// Source: https://developers.sensorup.com/tutorials/chart/
function getObservations(url) {
  $.getJSON(url, function(observations) {
    var data = $.map(observations.value, function(observation) {
        var timestamp = moment(observation.phenomenonTime).valueOf();
        return [[timestamp, parseFloat(observation.result)]];
    });
    data.sort(function(a, b) {
      return a[0] - b[0];
    });
  });
}

// Source: https://www.highcharts.com/blog/code-examples/dynamically-updated-data/
// ChartID is the ID of the div
// function createChart(chartID) {
//   Highcharts.stockChart(chartID, {
//     chart: {
//         events: {
//             load: function () {
//                 // set up the updating of the chart each second
//                 var series = this.series[0];
//                 setInterval(function () {
//                     var x = (new Date()).getTime(), // current time
//                         y = Math.round(Math.random() * 100);
//                     series.addPoint([x, y], true, true);
//                 }, 1000);
//             }
//         }
//     },
//     time: {
//         useUTC: false
//     },
//     rangeSelector: {
//         buttons: [{
//             count: 1,
//             type: 'minute',
//             text: '1M'
//         }, {
//             count: 5,
//             type: 'minute',
//             text: '5M'
//         }, {
//             type: 'all',
//             text: 'All'
//         }],
//         inputEnabled: false,
//         selected: 0
//     },
//     title: {
//         text: 'Live random data'
//     },
//     exporting: {
//         enabled: false
//     },
//     series: [{
//         name: 'Random data',
//         data: (function () {
//             // generate an array of random data
//             var data = [],
//                 time = (new Date()).getTime(),
//                 i;

//             for (i = -999; i <= 0; i += 1) {
//                 data.push([
//                     time + i * 1000,
//                     Math.round(Math.random() * 100)
//                 ]);
//             }
//             return data;
//         }())
//     }]
//   });
// }

function createChart(chartID) {
  console.log("Just entered funciton")
  var title = {
     text: 'Monthly Average Temperature'   
  };
  var subtitle = {
     text: 'Source: WorldClimate.com'
  };
  var xAxis = {
     categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  };
  var yAxis = {
     title: {
        text: 'Temperature (\xB0C)'
     },
     plotLines: [{
        value: 0,
        width: 1,
        color: '#808080'
     }]
  };   

  var tooltip = {
     valueSuffix: '\xB0C'
  }
  var legend = {
     layout: 'vertical',
     align: 'right',
     verticalAlign: 'middle',
     borderWidth: 0
  };
  var series =  [{
        name: 'Tokyo',
        data: [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2,
           26.5, 23.3, 18.3, 13.9, 9.6]
     }, 
     {
        name: 'New York',
        data: [-0.2, 0.8, 5.7, 11.3, 17.0, 22.0, 24.8, 
           24.1, 20.1, 14.1, 8.6, 2.5]
     }, 
     {
        name: 'Berlin',
        data: [-0.9, 0.6, 3.5, 8.4, 13.5, 17.0, 18.6,
           17.9, 14.3, 9.0, 3.9, 1.0]
     }, 
     {
        name: 'London',
        data: [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 
           16.6, 14.2, 10.3, 6.6, 4.8]
     }
  ];

  var json = {};
  json.title = title;
  json.subtitle = subtitle;
  json.xAxis = xAxis;
  json.yAxis = yAxis;
  json.tooltip = tooltip;
  json.legend = legend;
  json.series = series;

  chartID = '#' + chartID

  $(chartID).highcharts(json);
};