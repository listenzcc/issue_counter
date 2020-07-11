// Get Dates within year-month in [src]
function getDates(src) {
    // Output list of date object
    var DATES = [];

    // Parse input [src]
    var y, m;
    [y, m] = src.split('-');
    var year = parseInt(y);
    var month = parseInt(m) - 1;

    // Try each day,
    // if within the month, record into [DATES],
    // if out the month, break.
    var d;
    for (var date = 1; date < 35; date++) {
        // Make new date object
        d = new Date(year, month, date, 0);
        // Enter into next month,
        // break
        if (month != d.getMonth()) {
            break;
        }
        // Record the date
        DATES[date - 1] = d;
    }

    return DATES;
}

module.exports = getDates;