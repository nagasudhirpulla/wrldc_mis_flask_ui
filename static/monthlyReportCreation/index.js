const createMonthlyReport = function() {
    $.ajax({
        type: 'post',
        dataType: 'json',
        contentType: "application/json",
        data: JSON.stringify({}),
        success: function(resp) {

        },
        error: function(jqXHR, exception) {
            console.log(jqXHR);
            console.log(exception);
        }
    });
}

document.getElementById('createMonthlyReportBtn').onclick = createMonthlyReport