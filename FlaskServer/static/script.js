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
  if (comparator=="Less Than") {
    return operand1 < operand2
  } else if (comparator=="More Than") {
    return operand1 > operand2
  } else {
    return "Error in comparator name"
  }
}

function setAndcalculateState(dataForm, dataStreamID, comparator, limit, serverAddress, containerID) {
  if (dataForm == "Most Recent Value") {
    queryAddress = serverAddress + "/Datastreams" + "(" + dataStreamID + ")" + "/Observations?$top=1&$orderby=phenomenonTime desc"
    $.getJSON(queryAddress, function(results) {
      observationResult = parseFloat(results["result"])
      state = calculateState(observationResult, comparator, parseFloat(limit))

      document.getElementById(containerID).innerHTML = state
    })
  } else if (dataForm == "1 min Average") {

    let millesecondsToSubtract = 1000 * 60 // Totals 1 min
    resultsFromTime = getDateWithOffset(millesecondsToSubtract)

    queryAddress = serverAddress + "/Datastreams" + "(" + dataStreamID + ")" + "/Observations?$orderby=phenomenonTime desc&$filter=phenomenonTime ge " + resultsFromTime
    state = getResultsAndAverageState(queryAddress, comparator, limit, containerID)
  } else if (dataForm == "5 min Average") {

    let millesecondsToSubtract = 1000 * 60 * 5 // Totals 5 mins
    resultsFromTime = getDateWithOffset(millesecondsToSubtract)

    queryAddress = serverAddress + "/Datastreams" + "(" + dataStreamID + ")" + "/Observations?$orderby=phenomenonTime desc&$filter=phenomenonTime ge " + resultsFromTime
    state = getResultsAndAverageState(queryAddress, comparator, limit, containerID)
  } else if (dataForm == "1 hour Average") {
    
    let millesecondsToSubtract = 1000 * 60 * 60 // Totals 60 mins
    resultsFromTime = getDateWithOffset(millesecondsToSubtract)

    queryAddress = serverAddress + "/Datastreams" + "(" + dataStreamID + ")" + "/Observations?$orderby=phenomenonTime desc&$filter=phenomenonTime ge " + resultsFromTime
    state = getResultsAndAverageState(queryAddress, comparator, limit, containerID)
  }
}

function getResultsAndAverageState(queryAddress, comparator, limit, containerID) {
  $.getJSON(queryAddress, function(results) {
    numberOfObservations = results['value'].length

    // TODO Add loops for when observations are over 100 (i.e. another request is needed for the next set of results)
    if (numberOfObservations == 100) {
      console.log("Warning: Number of observations maxed, not using full data set")
    }
    
    if (numberOfObservations == 0) {
      state = "No Data"
    } else {
      runningTotal = 0
      for (let i=0; i<numberOfObservations; i++) {
        runningTotal += results['value'][i]['result']
      }
      mean = runningTotal / numberOfObservations
      state = calculateState(mean, comparator, parseFloat(limit))
    }
    document.getElementById(containerID).innerHTML = state
  })
}

function getDateWithOffset(millesecondsToSubtract) {
  let UTCStamp = new Date().getTime()
  let timeZoneOffset = new Date().getTimezoneOffset()*60*1000
  let getResultsFromDate = new Date(UTCStamp - millesecondsToSubtract - timeZoneOffset)
  return getResultsFromDate.toISOString()
}

function setDataStreamName(dataStreamID, serverAddress, containerID) {
  queryAddress = serverAddress + "/Datastreams" + "(" + dataStreamID + ")"
  $.getJSON(queryAddress, function(results) {
    document.getElementById(containerID).innerHTML = results["name"]
  }) 
}

function setDataStreamOptions(serverAddress, containerID) {
  queryAddress = serverAddress + "/Datastreams"
  $.getJSON(queryAddress, function(results) {

    dataStreams = results['value']
    dataStreams.sort(function(a, b) {
      return parseInt(a['@iot.id']) - parseInt(b['@iot.id'])
    })

    optionTags = ""
    for (let i=0; i<dataStreams.length; i++) {
      optionTags = optionTags + "<option>" + dataStreams[i]['@iot.id'] + " - " + dataStreams[i]['name'] + "</option>"
    }
    
    document.getElementById(containerID).innerHTML = optionTags
  }) 
}