jQuery(document).ready(function() {
    jQuery.ajax({
        url: script_args_single_etf_charts_init.ajaxUrl,
        method: 'POST',
        data: {
            action: 'get_nav_historical_data',
            pid: script_args_single_etf_charts_init.fundId,
        },
        success: function(responseData) {

            if( responseData.success === true && responseData.data.length > 0 ) {
                initFundNavHistoricalChart( responseData.data );
            } else {
                let graph = document.getElementById('js-graph');
                graph.style.display = 'none';
            }
        }
    }).done(function() {

        const choosedQtr = jQuery('.fund-premium-discount-date-selector').find('option:selected')
        const qtr = choosedQtr.data('qtr');
        const year = choosedQtr.data('year');
        jQuery.ajax({
            url: script_args_single_etf_charts_init.ajaxUrl,
            method: 'POST',
            data: {
                action: 'get_premium_discount_data',
                pid: script_args_single_etf_charts_init.fundId,
                qtr:qtr,
                year:year
            },
            success: function(responseData) {
                if( responseData.success === true) {
                    /*initFundPremiumDiscountChart( responseData.fundData )*/
                }
            }
        });
    });
});
