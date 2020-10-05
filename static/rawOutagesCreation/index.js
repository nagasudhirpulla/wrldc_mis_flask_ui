const createRawOutages = function() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const respSelector = "#respDiv";
    $(respSelector).text('Please wait...');
    $(respSelector).css('border-color', 'transparent');
    $.ajax({
        type: 'post',
        dataType: 'json',
        contentType: "application/json",
        data: JSON.stringify({ startDate: startDate, endDate: endDate }),
        success: function(resp) {
            var borderColor = 'red';
            if (resp.hasOwnProperty('isSuccess') && resp.hasOwnProperty('message')) {
                if (resp['isSuccess']) {
                    borderColor = 'green';
                }
                $(respSelector).text(resp['message']);
            } 
            else {
                $(respSelector).text(JSON.stringify(resp));
            }
            $(respSelector).css('border-color', borderColor);
            console.log(resp);
        },
        error: function(jqXHR, exception) {
            $(respSelector).css('border-color', 'red');
            $(respSelector).html(jqXHR.responseText);
            console.log(jqXHR);
            // console.log(exception);
        }
    });
}

document.getElementById('createRawOutagesBtn').onclick = createRawOutages