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

function getCurrentValueLoop(elementID, observationUrl, unitSymbol) {
  getAndSetCurrentValue(elementID, observationUrl, unitSymbol)
  setInterval(function () {
    getAndSetCurrentValue(elementID, observationUrl, unitSymbol)
  }, 3000);
}

function getAndSetCurrentValue(elementID, observationUrl, unitSymbol) {
  $.getJSON(observationUrl, function(observations) {
    var value = parseFloat(observations['value'][0]['result']).toFixed(2)

    document.getElementById(elementID).innerHTML = value + " " + unitSymbol
  });
}

function toggleVisibleGraphs(datastreamID) {
  var x = document.getElementById("chart-" + datastreamID);
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
  var x = document.getElementById("currentValueContainer-" + datastreamID);
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
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

function refreshStatesLoop(dataForm, dataStreamID, comparator, limit, serverAddress, containerID) {
  setAndcalculateState(dataForm, dataStreamID, comparator, limit, serverAddress, containerID)
  setInterval(function () {
    setAndcalculateState(dataForm, dataStreamID, comparator, limit, serverAddress, containerID)
  }, 5000);
}

function setAndcalculateState(dataForm, dataStreamID, comparator, limit, serverAddress, containerID) {
  if (dataForm == "Most Recent Value") {
    queryAddress = serverAddress + "/Datastreams" + "(" + dataStreamID + ")" + "/Observations?$top=1&$orderby=phenomenonTime desc"
    $.getJSON(queryAddress, function(results) {
      observationResult = parseFloat(results['value'][0]["result"])
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

async function getAllValues(queryAddress) {
  const response = await fetch(queryAddress)
  var results = await response.json();

  var resultsList = []
  if (results['@iot.nextLink'] != undefined) {
    resultsList = await getAllValues(results['@iot.nextLink'])
  }

  numberOfObservations = results['value'].length
  for (let i=0; i<numberOfObservations; i++) {
    resultsList.push(results['value'][i]['result'])
  }

  return resultsList
}

function getResultsAndAverageState(queryAddress, comparator, limit, containerID) {
  $.getJSON(queryAddress, async function(results) {
    numberOfObservations = results['value'].length

    if (numberOfObservations == 0) {
      state = "No Data"
    } else {
      fullList = await getAllValues(queryAddress) // Get any extra results from nextLink
      runningTotal = 0
      for (let i=0; i<fullList.length; i++) {
        runningTotal += fullList[i]
      }
      mean = runningTotal / fullList.length
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