function downloadFile(fileUrl, fileName) {
    let a = document.createElement("a");
    a.href = fileUrl;
    a.setAttribute("download", fileName);
    a.click();
}

function initFundNavHistoricalChart( fundData ) {
    if( ! fundData || typeof fundData === undefined || fundData.length === 0) {
        return true;
    }

    new Highcharts.stockChart({
        series: fundData,
        chart: {
            renderTo: 'nav_chart',
            height: 420,
            backgroundColor: 'transparent',
            borderWidth: 0,
            plotBackgroundColor: 'transparent',
            plotShadow: false,
            plotBorderWidth: 0,
            margin: [23, 45, 0, 0],
            padding: [0, 0, 0, 0],
            spacing: [20, 1, 2, 25],
            style: {
                font: '"Arimo","HelveticaNeue","Helvetica Neue",Helvetica,Arial,sans-serif'
            }
        },

        plotOptions: {
            series: {
                animation: false
            },
            column: {
                borderWidth: 0,
                borderColor: 'transparent',
                shadow: false,
            }
        },
        rangeSelector: {
            selected: 2,
            buttonSpacing: 20,
            inputEnabled: false,
            labelStyle: {
                fontSize: '20px',
                fontFamily: '"Brother 1816"',
                color: '#7D808E',
                transform: 'translateX(-10px)'
            },
            buttonPosition:{
                x: 10,
            },
            buttonTheme: {
                fill: 'none',
                stroke: 'none',
                width: '46px',
                style: {
                    color: '#7D808E',
                    fontWeight: 'bold',
                    fontSize: '20px',
                    fontFamily: '"Brother 1816"'
                },
                states: {
                    hover: {
                        style: {
                            color: '#38D996'
                        }
                    },
                    select: {
                        style: {
                            color: '#38D996'
                        }
                    },
                    disabled: {
                        style: {
                            color: '#313131'
                        }
                    }
                }
            }
        },

        colors: ['#38D996', '#38D996'],
        yAxis: {
            allowDecimals: true,
            tickInterval: 2,
            labels: {
                align: 'left',
                marginRight: 10,
                formatter: function () {
                    return '$' + this.value;
                },
            },
            gridLineColor: 'rgba(192, 192, 192, 0.2)',
            plotLines: [{
                value: 0,
                width: 1,
                color: 'rgba(192, 192, 192, 0.2)'
            }]
        },

        credits: {
            enabled: false
        },

        legend: {
            enabled: false
        },
        navigator: {
            enabled: false,
        },
        tooltip: {
            borderColor: '#678CB7',
            borderRadius: 0,
            pointFormat: getTooltipPointFormat('$'),
            valueDecimals: 2,
            xDateFormat: '%m/%d/%Y'
        },
    });
}

function initFundPremiumDiscountChart( fundData ) {
    if( ! fundData || typeof fundData === undefined) {
        return true;
    }

    new Highcharts.stockChart({
        series: [ fundData ],
        chart: {
            renderTo: 'pd_chart',
            height: 440,
            backgroundColor: 'transparent',
            borderWidth: 0,
            plotBackgroundColor: 'transparent',
            plotShadow: false,
            plotBorderWidth: 0,
            margin: [30, 0, 30, 90],
            padding: [0, 0, 0, 20],
            spacing: [20, 1, 2, 25],
            style: {
                font: '"Arimo","HelveticaNeue","Helvetica Neue",Helvetica,Arial,sans-serif'
            }
        },

        plotOptions: {
            series: {
                animation: false
            },
            column: {
                borderWidth: 0,
                borderColor: 'transparent',
                shadow: false,
            }
        },

        rangeSelector: {
            enabled: false
        },

        navigator: {
            enabled: false
        },

        scrollbar: {
            enabled: false
        },

        colors: ['#6A4BFF', '#6A4BFF'],

        yAxis: {
            showFirstLabel: true,
            opposite: false,
            title: {
                text: "Premium/Discount Range (%)",
                margin: 0,
                x: -20
            },
            allowDecimals: true,
            tickInterval: 0.5,
            labels: {
                align: 'center',
                y: 4,
                formatter: function () {
                    return this.value + '%';
                },
            },
            gridLineColor: 'rgba(192, 192, 192, 0.2)',
            plotLines: [{
                value: 0,
                width: 1,
                color: 'rgba(192, 192, 192, 0.2)'
            }],
            min: -2.0,
            max: 2.0
        },

        credits: {
            enabled: false
        },

        legend: {
            enabled: false
        },

        tooltip: {
            borderColor: '#678CB7',
            borderRadius: 0,
            pointFormat: getTooltipPointFormat('%'),
            valueDecimals: 2,
            xDateFormat: '%m/%d/%Y'
        },
    });
}

function getTooltipPointFormat(formatSymbol) {
    let formattedValue = '';

    if(formatSymbol === '$') {
        formattedValue = formatSymbol + '{point.y}';
    } else if(formatSymbol === '%') {
        formattedValue = '{point.y}' + formatSymbol;
    }
    return `<span style="color:{series.color}; font-weight:600">{series.name}</span>: <b>${formattedValue}</b>`;
}