// Source: https://developers.sensorup.com/tutorials/chart/
function formatData(observations) {
  var data = $.map(observations.value, function(observation) {
    var timestamp = moment(observation.phenomenonTime).valueOf();
    return [[timestamp, parseFloat(observation.result)]];
  });
  data.sort(function(a, b) {
    return a[0] - b[0];
  });
  return data
}

function createChartObject(chartID, observationUrl, name, unitSymbol, unitName) {

  $.getJSON(observationUrl, function(observations) {
    var data = formatData(observations)

    var chart = new Highcharts.StockChart(chartID, {
      title: { text: "Loading Chart Data..." },
      series: [],
      chart: {
        events: {
          load: function () {
            // 'this' contains the chart object but is unreachable in the next funciton's scope unless defined here
            var series = this.series
            setInterval(function () {
                $.getJSON(observationUrl, function(observations) {
                    var data = formatData(observations)
                    series[0].setData(data, redraw=true)
                })
            }, 5000);
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

function calculateState(operand1, comparator, operand2) {
  if (comparator="lessThan") {
    return operand1 < operand2
  } else if (comparator="moreThan") {
    return operand1 > operand2
  } else {
    return "Error in comparator name"
  }
}

function setAndcalculateState(dataForm, dataStreamID, comparator, limit, serverAddress, containerID) {
  if (dataForm == "mostRecent") {
    queryAddress = serverAddress + "/Datastreams" + "(" + dataStreamID + ")" + "/Observations?$top=1&$orderby=phenomenonTime desc"
    $.getJSON(queryAddress, function(results) {
      observationResult = parseFloat(results["result"])
      state = calculateState(observationResult, comparator, parseFloat(limit))

      document.getElementById(containerID).innerHTML = state
    })
  }
}

function setDataStreamName(dataStreamID, serverAddress, containerID) {
  queryAddress = serverAddress + "/Datastreams" + "(" + dataStreamID + ")"
  $.getJSON(queryAddress, function(results) {
    document.getElementById(containerID).innerHTML = results["name"]
  }) 
}