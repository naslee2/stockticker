$(document).ready(function(){
    $.getJSON("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=RTN&apikey=67ZBM9BPG298O6TL", function(res) {
        console.log(res);
    }, "json");
});