function load_stats(selector, grouping){

    init_progress()
    var lines = []
    var series = []
    $.ajax({
        url: "{%url 'stats_temperature'%}" + grouping,
        dataType: "json",
        beforeSend: function(){progress(30)},
        complete: function(){$("[title!=undefined]").tooltip({"animation": "true"});progress(100)},
        error: function(ob){show_msg(ob.responseText)}
        success: function(data){
            $.each(data, function(k, v){
                series.push({label: k})
                lines.push([])

                $.each(v, function(k, vv){

                    var d = new Date(0);
                    d.setUTCSeconds(k);

                    var i = lines.length -1
                    if (lines[i] == "undefined") lines[i ] = []
                    lines[i].push([d, vv ])
                    delete d, i;
                })

            })
            //console.log(lines)
            //console.log(series)
            $.jqplot(selector, lines, {
                  title:'Temperature evolution for last ' + grouping,
                  // Series options are specified as an array of objects, one object
                  // for each series.
                  seriesDefaults:{
                      shadowAlpha: 0.2,
                      lineWidth:2,
                      markerOptions: { show: false }
                  },
                  series: series,
                        legend: {
                          show: true,
                          location: 'nw',
                          placement: 'inside',
                        fontSize: '11px'
                    } ,
                highlighter: {
                    lineWidthAdjust: 2.5,   // pixels to add to the size line stroking the data point marker
                                            // when showing highlight.  Only affects non filled data point markers.
                    sizeAdjust: 5,          // pixels to add to the size of filled markers when drawing highlight.
                    showTooltip: true,      // show a tooltip with data point values.
                    tooltipLocation: 'nw',  // location of tooltip: n, ne, e, se, s, sw, w, nw.
                    fadeTooltip: true,      // use fade effect to show/hide tooltip.
                    tooltipFadeSpeed: "fast"// slow, def, fast, or a number of milliseconds.
                    tooltipOffset: 2,       // pixel offset of tooltip from the highlight.
                    tooltipAxes: 'both',    // which axis values to display in the tooltip, x, y or both.
                    tooltipSeparator: ', '  // separator between values in the tooltip.
                    useAxesFormatters: true // use the same format string and formatters as used in the axes to
                                            // display values in the tooltip.
                    tooltipFormatString: '%.5P' // sprintf format string for the tooltip.  only used if
                                                // useAxesFormatters is false.  Will use sprintf formatter with
                                                // this string, not the axes formatters.
                },


                axes: {
                    // options for each axis are specified in seperate option objects.
                    xaxis: {
                      label: "Date",
                      renderer:$.jqplot.DateAxisRenderer,
                    },
                    yaxis: {
                      label: "Temperature(celsius)"
                    }
                  }
                })

        },

    })
    delete lines, series;
    drop_progress();

}
