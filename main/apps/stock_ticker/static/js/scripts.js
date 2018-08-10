var stock_data = {};

$(document).ready(function(){
    stock_data.symbol = "RTN";
    stock_data.function = "TIME_SERIES_DAILY";

    $("form").submit(function(e){
        e.preventDefault();
        stock_data.symbol = $("#symbol").val();
        stock_data.function  = $("#time_series option:selected").val();
        stocks();
    })

    // setInterval(function(){
    //     stocks();
    // }, 600000);
});

function stocks(){
    $.getJSON("https://www.alphavantage.co/query?function="+stock_data.function+"&symbol="+stock_data.symbol+"&apikey=67ZBM9BPG298O6TL", function(request) {
            if(request['Error Message']){
                console.log(request['Error Message'])
            }
            else{
                console.log(request); 
            }
        });
}

// var crypto_data = {};
// var fx_data = {};

    // crypto_data.function = "DIGITAL_CURRENCY_INTRADAY";
    // crypto_data.market = "EUR";
    // crypto_data.symbol = "BTC";

    // fx_data.function = "CURRENCY_EXCHANGE_RATE"
    // fx_data.from_currency = "USD"
    // fx_data.to_currency = "JPY"

// function crypto(){
//     $.getJSON("https://www.alphavantage.co/query?function="+crypto_data.function+"&symbol="+crypto_data.symbol+"&market=EUR&apikey=67ZBM9BPG298O6TL", function(request) {
//         console.log(crypto_data.function, request);
//         }, "json");
// }

// function fx(){
//     $.getJSON("https://www.alphavantage.co/query?function="+fx_data.function+"&from_currency="+fx_data.from_currency+"&to_currency="+fx_data.to_currency+"&apikey=67ZBM9BPG298O6TL", function(request) {
//         console.log(fx_data.function, request['Realtime Currency Exchange Rate']);
        
//         $("#from_currency_name").html(request['Realtime Currency Exchange Rate']['2. From_Currency Name']);

//         $("#to_currency_name").html(request['Realtime Currency Exchange Rate']['4. To_Currency Name']);

//         $("#from_currency").html("1");
//         $("#to_currency").html(request['Realtime Currency Exchange Rate']['5. Exchange Rate']);

//         }, "json");
// }



