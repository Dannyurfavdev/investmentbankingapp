let arkCharts = {
    barChart: function (data, chartTitle, chartXLabel, chartYLabel, chartSourceLabel, chartLegend) {
        // set the dimensions and margins of the graph
        const margin = {top: 90, right: 30, bottom: 90, left: 80};
        let width = 690 - margin.left - margin.right;
        let height = 600 - margin.top - margin.bottom;

        if (window.innerWidth < 768) {
            width = 330 - margin.left - margin.right;
            height = 300 - margin.top - margin.bottom;
        }

        // append the svg object to the body of the page
        const svg = d3.select(".wp-chart")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .attr("max-width", "100%")
            .append("g")
            .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");

        // TODO: Replace this line with our data. Our data for chart stored in global scope in variable chartData
        // get the data
        //d3.csv("https://raw.githubusercontent.com/holtzy/data_to_viz/master/Example_dataset/1_OneNum.csv", function(data2) {

            const data3 = JSON.parse(data);
            const legend = JSON.parse(chartLegend);

            // X axis: scale and draw:
            const x = d3.scaleLinear()
                .domain([0, 1000])     // can use this instead of 1000 to have the max of data: d3.max(data, function(d) { return +d.price })
                .range([0, width]);
            svg.append("g")
                .attr("class", "axisX")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(x));

            const axisXPath = document.querySelector(".axisX path");
            const axisXLines = document.querySelectorAll(".axisX .tick line");
            const axisXTexts = document.querySelectorAll(".axisX .tick text");
            axisXPath.style.stroke = "#dee0e6";
            axisXLines.forEach(function (el)
            {
                el.style.stroke = "transparent";
            });
            axisXLines[0].style.stroke = "#F2F3F6";
            axisXLines[axisXLines.length-1].style.stroke = "#F2F3F6";
            axisXTexts.forEach(function (el)
            {
                el.style.fontSize = "11px";
            });

            // set the parameters for the histogram
            const histogram = d3.histogram()
                .value(function(d) { return d.price; })   // I need to give the vector of value
                .domain(x.domain())  // then the domain of the graphic
                .thresholds(x.ticks(70)); // then the numbers of bins

            // And apply this function to data to get the bins
            const bins = histogram(data3);

            // Y axis: scale and draw:
            const y = d3.scaleLinear()
                .range([height, 0]);
            y.domain([0, d3.max(bins, function(d) { return d.length; })]);   // d3.hist has to be called before the Y axis obviously
            svg.append("g")
                .attr("class", "axisY")
                .call(d3.axisLeft(y));

            const axisYPath = document.querySelector(".axisY path");
            const axisYLines = document.querySelectorAll(".axisY .tick line");
            const axisYTexts = document.querySelectorAll(".axisY .tick text");
            axisYPath.style.stroke = "transparent";
            axisYLines.forEach(function (el)
            {
                el.style.stroke = "#F2F3F6";
            });
            axisYTexts.forEach(function (el)
            {
                el.style.fontSize = "11px";
            });

            if (chartXLabel) {
                // Add X axis label:
                svg.append("text")
                    .attr("text-anchor", "middle")
                    .attr("x", width/2)
                    .attr("y", height + 50)
                    .style("color", "#737887")
                    .style("font-size", "12px")
                    .style("font-weight", "600")
                    .text(chartXLabel);
            }

            if (chartYLabel) {
                // Y axis label:
                svg.append("text")
                    .attr("text-anchor", "middle")
                    .attr("transform", "rotate(-90)")
                    .attr("y", -50)
                    .attr("x", -height/2)
                    .style("color", "#737887")
                    .style("font-size", "12px")
                    .style("font-weight", "600")
                    .text(chartYLabel);
            }

            if (chartSourceLabel) {
                // Add Source label:
                svg.append("text")
                    .attr("text-anchor", "middle")
                    .attr("x", width/2)
                    .attr("y", height + 80)
                    .style("color", "#7D808E")
                    .style("font-family", "Caecilia")
                    .style("font-size", "13px")
                    .style("font-weight", "500")
                    .style("line-height", "17px")
                    .text(chartSourceLabel);
            }

            if(chartTitle) {
                //Add title
                svg.append("text")
                    .attr("x", (width / 2))
                    .attr("y", 0 - margin.top + 30)
                    .attr("text-anchor", "middle")
                    .style("font-size", "23px")
                    .style("font-weight", "700")
                    .style("color", "#737887")
                    .text(chartTitle);
            }

        // let legendItems = 0;
        // for(let key in legend) {
        //     if(legend[key].text) {
        //         legendItems = legendItems + 1;
        //     }
        // }
        // const aa = (100/legendItems)/2 + '%';

        // const legendGroup = svg.append("g")
        //     .attr("class", "legend");
        //     //.style("transform", `translateX(${aa})`);

        const legendGroup = svg.append("g")
            .attr("class", "legend");

        const sl = 12;

        if (legend[0].text) {
                legendGroup.append("circle")
                    .attr("cx", 0)
                    .attr("cy", 0 - margin.top + 60)
                    .attr("r", 5)
                    .style("fill", legend[0].color);
                legendGroup.append("text")
                    .attr("x", 10)
                    .attr("y", 0 - margin.top + 60)
                    .text(legend[0].text)
                    .style("color", "#737887")
                    .style("font-size", "12px")
                    .style("font-weight", "600")
                    .attr("alignment-baseline","middle");
            }

            if (legend[1].text) {
                legendGroup.append("circle")
                    .attr("cx",legend[0].text.length*sl)
                    .attr("cy", 0 - margin.top + 60)
                    .attr("r", 5)
                    .style("fill", legend[1].color);
                legendGroup.append("text")
                    .attr("x", 10  + legend[0].text.length*sl)
                    .attr("y", 0 - margin.top + 60)
                    .text(legend[1].text)
                    .style("color", "#737887")
                    .style("font-size", "12px")
                    .style("font-weight", "600")
                    .attr("alignment-baseline","middle");
            }

        if (legend[2].text) {
            legendGroup.append("circle")
                .attr("cx",legend[0].text.length*sl + legend[1].text.length*sl)
                .attr("cy", 0 - margin.top + 60)
                .attr("r", 5)
                .style("fill", legend[2].color);
            legendGroup.append("text")
                .attr("x", 10  + legend[0].text.length*sl + legend[1].text.length*sl)
                .attr("y", 0 - margin.top + 60)
                .text(legend[2].text)
                .style("color", "#737887")
                .style("font-size", "12px")
                .style("font-weight", "600")
                .attr("alignment-baseline","middle");
        }

        if (legend[3].text) {
            legendGroup.append("circle")
                .attr("cx",legend[0].text.length*sl + legend[1].text.length*sl + legend[2].text.length*sl)
                .attr("cy", 0 - margin.top + 60)
                .attr("r", 5)
                .style("fill", legend[3].color);
            legendGroup.append("text")
                .attr("x", 10  + legend[0].text.length*sl + legend[1].text.length*sl + legend[2].text.length*sl)
                .attr("y", 0 - margin.top + 60)
                .text(legend[3].text)
                .style("color", "#737887")
                .style("font-size", "12px")
                .style("font-weight", "600")
                .attr("alignment-baseline","middle");
        }

        if (legend[4].text) {
            legendGroup.append("circle")
                .attr("cx",legend[0].text.length*sl + legend[1].text.length*sl + legend[2].text.length*sl + legend[3].text.length*sl)
                .attr("cy", 0 - margin.top + 60)
                .attr("r", 5)
                .style("fill", legend[4].color);
            legendGroup.append("text")
                .attr("x", 10  + legend[0].text.length*sl + legend[1].text.length*sl + legend[2].text.length*sl + legend[3].text.length*sl)
                .attr("y", 0 - margin.top + 60)
                .text(legend[4].text)
                .style("color", "#737887")
                .style("font-size", "12px")
                .style("font-weight", "600")
                .attr("alignment-baseline","middle");
        }


            // append the bar rectangles to the svg element
            svg.selectAll("rect")
                .data(bins)
                .enter()
                .append("rect")
                .attr("x", 1)
                .attr("transform", function(d) { return "translate(" + x(d.x0) + "," + y(d.length) + ")"; })
                .attr("width", function(d) { return x(d.x1) - x(d.x0) -1 ; })
                .attr("height", function(d) { return height - y(d.length); })
                .style("fill", "#8264ff");
                //.style("fill", function(d){ if(d.x0<140){return "#8264ff"} else {return "#38d996"}});

        //});
    },

    lineChart: function (data, chartTitle, chartXLabel, chartYLabel, chartSourceLabel, chartLegend) {

        // set the dimensions and margins of the graph
        const margin = {top: 90, right: 70, bottom: 90, left: 80};
        let width = 690 - margin.left - margin.right;
        let height = 600 - margin.top - margin.bottom;

        if (window.innerWidth < 768) {
            width = 330 - margin.left - margin.right;
            height = 300 - margin.top - margin.bottom;
        }

        // append the svg object to the body of the page
        const svg = d3.select(".wp-chart")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");

        // TODO: Replace this line with our data. Our data for chart stored in global scope in variable chartData
        //Read the data
        // d3.csv("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/data_connectedscatter.csv", function(data2) {

            const data3 = JSON.parse(data);
            const legend = JSON.parse(chartLegend);

            // List of groups (here I have one group per column)
            const allGroup = ["valueA", "valueB", "valueC"];
            const allColors = ["#8264ff", "#38d996", "#f74870"];

            // Reformat the data: we need an array of arrays of {x, y} tuples
            const dataReady = allGroup.map( function(grpName) { // .map allows to do something for each element of the list
                return {
                    name: grpName,
                    values: data3.map(function(d) {
                        return {time: d.time, value: +d[grpName]};
                    })
                };
            });

            //console.log(dataReady);

            // A color scale: one color for each group
            let myColor = d3.scaleOrdinal()
                .domain(allGroup)
                .range(allColors);

            // Add X axis --> it is a date format
            const x = d3.scaleLinear()
                .domain([0,10])
                .range([ 0, width ]);
            svg.append("g")
                .attr("class", "axisX")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(x));

            const axisXPath = document.querySelector(".axisX path");
            const axisXLines = document.querySelectorAll(".axisX .tick line");
            const axisXTexts = document.querySelectorAll(".axisX .tick text");
            axisXPath.style.stroke = "#dee0e6";
            axisXLines.forEach(function (el)
            {
                el.style.stroke = "transparent";
            });
            axisXLines[0].style.stroke = "#F2F3F6";
            axisXLines[axisXLines.length-1].style.stroke = "#F2F3F6";
            axisXTexts.forEach(function (el)
            {
                el.style.fontSize = "11px";
            });


            // Add Y axis
            const y = d3.scaleLinear()
                .domain( [0,20])
                .range([ height, 0 ]);
            svg.append("g")
                .attr("class", "axisY")
                .call(d3.axisLeft(y));

            const axisYPath = document.querySelector(".axisY path");
            const axisYLines = document.querySelectorAll(".axisY .tick line");
            const axisYTexts = document.querySelectorAll(".axisY .tick text");
            axisYPath.style.stroke = "transparent";
            axisYLines.forEach(function (el)
            {
                el.style.stroke = "#F2F3F6";
            });
            axisYTexts.forEach(function (el)
            {
                el.style.fontSize = "11px";
            });

            // Add a legend at the end of each line
            svg
                .selectAll("myLabels")
                .data(dataReady)
                .enter()
                .append('g')
                .append("text")
                .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; }) // keep only the last value of each time series
                .attr("transform", function(d) { return "translate(" + x(d.value.time) + "," + y(d.value.value) + ")"; }) // Put the text at the position of the last point
                .attr("x", 12) // shift the text a bit more right
                .text(function(d) { return d.name; })
                .style("fill", "#737887")
                .style("font-size", 13);

            if (chartXLabel) {
                // Add X axis label:
                svg.append("text")
                    .attr("text-anchor", "end")
                    .attr("x", width/2 + 3*chartXLabel.length)
                    .attr("y", height + 50)
                    .style("color", "#737887")
                    .style("font-size", "12px")
                    .style("font-weight", "600")
                    .text(chartXLabel);
            }

            if (chartYLabel) {
                // Y axis label:
                svg.append("text")
                    .attr("text-anchor", "end")
                    .attr("transform", "rotate(-90)")
                    .attr("y", -50)
                    .attr("x", -height/2 + 3*chartYLabel.length)
                    .style("color", "#737887")
                    .style("font-size", "12px")
                    .style("font-weight", "600")
                    .text(chartYLabel);
            }

            if (chartSourceLabel) {
                // Add Source label:
                svg.append("text")
                    .attr("text-anchor", "end")
                    .attr("x", width/2 + 3*chartSourceLabel.length)
                    .attr("y", height + 80)
                    .style("color", "#7D808E")
                    .style("font-family", "Caecilia")
                    .style("font-size", "13px")
                    .style("font-weight", "500")
                    .style("line-height", "17px")
                    .text(chartSourceLabel);
            }

            if(chartTitle) {
                //Add title
                svg.append("text")
                    .attr("x", (width / 2))
                    .attr("y", 0 - margin.top + 30)
                    .attr("text-anchor", "middle")
                    .style("font-size", "23px")
                    .style("font-weight", "700")
                    .style("color", "#737887")
                    .text(chartTitle);
            }

        const legendGroup = svg.append("g")
            .attr("class", "legend");

        const sl = 12;

        if (legend[0].text) {
            legendGroup.append("circle")
                .attr("cx", 0)
                .attr("cy", 0 - margin.top + 60)
                .attr("r", 5)
                .style("fill", legend[0].color);
            legendGroup.append("text")
                .attr("x", 10)
                .attr("y", 0 - margin.top + 60)
                .text(legend[0].text)
                .style("color", "#737887")
                .style("font-size", "12px")
                .style("font-weight", "600")
                .attr("alignment-baseline","middle");
        }

        if (legend[1].text) {
            legendGroup.append("circle")
                .attr("cx",legend[0].text.length*sl)
                .attr("cy", 0 - margin.top + 60)
                .attr("r", 5)
                .style("fill", legend[1].color);
            legendGroup.append("text")
                .attr("x", 10  + legend[0].text.length*sl)
                .attr("y", 0 - margin.top + 60)
                .text(legend[1].text)
                .style("color", "#737887")
                .style("font-size", "12px")
                .style("font-weight", "600")
                .attr("alignment-baseline","middle");
        }

        if (legend[2].text) {
            legendGroup.append("circle")
                .attr("cx",legend[0].text.length*sl + legend[1].text.length*sl)
                .attr("cy", 0 - margin.top + 60)
                .attr("r", 5)
                .style("fill", legend[2].color);
            legendGroup.append("text")
                .attr("x", 10  + legend[0].text.length*sl + legend[1].text.length*sl)
                .attr("y", 0 - margin.top + 60)
                .text(legend[2].text)
                .style("color", "#737887")
                .style("font-size", "12px")
                .style("font-weight", "600")
                .attr("alignment-baseline","middle");
        }

        if (legend[3].text) {
            legendGroup.append("circle")
                .attr("cx",legend[0].text.length*sl + legend[1].text.length*sl + legend[2].text.length*sl)
                .attr("cy", 0 - margin.top + 60)
                .attr("r", 5)
                .style("fill", legend[3].color);
            legendGroup.append("text")
                .attr("x", 10  + legend[0].text.length*sl + legend[1].text.length*sl + legend[2].text.length*sl)
                .attr("y", 0 - margin.top + 60)
                .text(legend[3].text)
                .style("color", "#737887")
                .style("font-size", "12px")
                .style("font-weight", "600")
                .attr("alignment-baseline","middle");
        }

        if (legend[4].text) {
            legendGroup.append("circle")
                .attr("cx",legend[0].text.length*sl + legend[1].text.length*sl + legend[2].text.length*sl + legend[3].text.length*sl)
                .attr("cy", 0 - margin.top + 60)
                .attr("r", 5)
                .style("fill", legend[4].color);
            legendGroup.append("text")
                .attr("x", 10  + legend[0].text.length*sl + legend[1].text.length*sl + legend[2].text.length*sl + legend[3].text.length*sl)
                .attr("y", 0 - margin.top + 60)
                .text(legend[4].text)
                .style("color", "#737887")
                .style("font-size", "12px")
                .style("font-weight", "600")
                .attr("alignment-baseline","middle");
        }

            function make_x_gridlines() {
                return d3.axisBottom(x)
                    .ticks(5)
            }

            function make_y_gridlines() {
                return d3.axisLeft(y)
                    .ticks(10)
            }

            // svg.append("g")
            //     .attr("class", "grid")
            //     .attr("transform", "translate(0," + height + ")")
            //     .call(make_x_gridlines()
            //         .tickSize(-height)
            //         .tickFormat("")
            //     )

            svg.append("g")
                .attr("class", "grid")
                .call(make_y_gridlines()
                    .tickSize(-width)
                    .tickFormat("")
                );

            const gridY = document.querySelector(".grid .domain");
            gridY.style.stroke = "transparent";

            const gridX = document.querySelectorAll(".grid .tick line");
            gridX.forEach(function (el)
            {
                el.style.stroke = "#dee0e6";
            });

            const gridXFirst = document.querySelectorAll(".grid .tick line");
            gridXFirst[0].style.stroke = "transparent";

            // Add the lines
            const line = d3.line()
                .x(function(d) { return x(+d.time) })
                .y(function(d) { return y(+d.value) })
            svg.selectAll("myLines")
                .data(dataReady)
                .enter()
                .append("path")
                .attr("d", function(d){ return line(d.values) } )
                .attr("stroke", function(d){ return myColor(d.name) })
                .style("stroke-width", 4)
                .style("fill", "none");

            // // Add the points
            // svg
            // // First we need to enter in a group
            //     .selectAll("myDots")
            //     .data(dataReady)
            //     .enter()
            //     .append('g')
            //     .style("fill", function(d){ return myColor(d.name) })
            //     // Second we need to enter in the 'values' part of this group
            //     .selectAll("myPoints")
            //     .data(function(d){ return d.values })
            //     .enter()
            //     .append("circle")
            //     .attr("cx", function(d) { return x(d.time) } )
            //     .attr("cy", function(d) { return y(d.value) } )
            //     .attr("r", 3)
            //     .attr("stroke", "#737887");

       // })

    }

};


const element = document.querySelector(".wp-chart");

if(element !== null){
    element.style.opacity = "0.1";
}
function unfade(element) {
    let op = 0.1;
    element.style.display = 'block';
    const timer = setInterval(function () {
        if (op >= 1){
            clearInterval(timer);
        }
        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ")";
        op += op * 0.3;
    }, 10);
}

document.addEventListener('DOMContentLoaded', function(){
    if (typeof chartType !== 'undefined') {
        if (chartType === 'barChart') {
            arkCharts.barChart(chartData, chartTitle, chartXLabel, chartYLabel, chartSourceLabel, chartLegend);
            unfade(element);
        } else if (chartType === 'lineChart') {
            arkCharts.lineChart(chartData, chartTitle, chartXLabel, chartYLabel, chartSourceLabel, chartLegend);
            unfade(element);
        } else {
            console.log("Selected chart type isn't supported yet.");
        }
    }

});
