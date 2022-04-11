// Source: https://developers.sensorup.com/tutorials/chart/
function getObservations(url) {
  $.getJSON(url, function(observations) {
    var data = $.map(observations.value, function(observation) {
        var timestamp = moment(observation.phenomenonTime).valueOf();
        observationTuple = [[timestamp, parseFloat(observation.result)]]
        return observationTuple;
    });
    data.sort(function(a, b) {
      return a[0] - b[0];
    });
  });
}

// Source: https://www.highcharts.com/blog/code-examples/dynamically-updated-data/

function onLoad(observationUrl) {
  console.log("Called on load for: " + observationUrl)

  // Add method to update series based on code below

  // set up the updating of the chart each second
  // var series = this.series[0];
  // setInterval(function () {
  //     var x = (new Date()).getTime(), // current time
  //         y = Math.round(Math.random() * 100);
  //     series.addPoint([x, y], true, true);
  // }, 1000);
}

function createChartObject(chartID, observationUrl, name, unitSymbol, unitName) {

  $.getJSON(observationUrl, function(observations) {
    var data = $.map(observations.value, function(observation) {
        var timestamp = moment(observation.phenomenonTime).valueOf();
        return [[timestamp, parseFloat(observation.result)]];
    });
    data.sort(function(a, b) {
      return a[0] - b[0];
    });

    var chart = new Highcharts.StockChart(chartID, {
      title: { text: "Loading Chart Data..." },
      series: [],
      chart: {
        events: {
          load: function() {
            onLoad(observationUrl)
          }
        }
      }
    });

    chart.showLoading();

    chart.setTitle({ text: name });

    var series = chart.addSeries({
      data: data,
      tooltip: {
        valueSuffix: " " + unitSymbol
      }
    });

    series.yAxis.update({
      title: {
        text: unitName + " (" + unitSymbol + ")"
      }
    });

    chart.hideLoading();

  });
}