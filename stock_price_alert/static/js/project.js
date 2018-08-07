/* Project specific Javascript goes here. */
var $TABLE = $('#table');
var $BTN = $('#export-btn');
var $EXPORT = $('#export');

$('.table-add').click(function () {
    var $clone = $TABLE.find('#new-row').clone(true).removeClass('hide table-line');
    $TABLE.find('table').append($clone);
    $(document).find('.add-button-show').removeClass("d-none hide");
});

$('.table-remove').click(function () {
    $(this).parents('tr').detach();
    let url = '/alerts/remove_alert/';
    let method = 'POST';
    let data = {};
    if(user!=='')
    {
            data['user_id'] = user;
    }
    data['uuid'] = $(this).data("id");
    helperMethods.secureHTTPRequestHandler(url, method, data, function (response) {
        $("#sideModalTR").on("shown.bs.modal", function () {  //Tell what to do on modal open
             $(this).find('#myModalLabel').html('Voila!!');
             $(this).find('.modal-body').html('Alert removed successfully.');
        }).modal('show');

    }, function (response, status, error) {
        $("#sideModalTR").on("shown.bs.modal", function () {  //Tell what to do on modal open
             $(this).find('#myModalLabel').html('Oops!!');
             $(this).find('.modal-body').html(response.message);
        }).modal('show');
    })


});


// A few jQuery helpers for exporting only
jQuery.fn.pop = [].pop;
jQuery.fn.shift = [].shift;

$BTN.click(function () {
    var $rows = $TABLE.find('tr:not(:hidden)');
    var headers = [];
    var data = [];


    // Get the headers (add special header logic here)
    $($rows.shift()).find('th:not(:empty)').each(function () {
        headers.push($(this).text().toLowerCase().replace(' ', '_'));
    });

    // Turn all existing rows into a loopable array
    $rows.each(function () {
        var $td = $(this).find('td');
        var h = {};

        // Use the headers from earlier to name our hash keys
        headers.forEach(function (header, i) {
            if($td.eq(i).find('.form-check-input').length){
                h[header] = $td.eq(i).find('.form-check-input').prop('checked');
            }
            else
            {
                h[header] = $td.eq(i).text();
            }

        });
        if(user!==''){
            h['user_id'] = user;
        }
        if(h['percentage']==='None'){
            delete h['percentage']
        }
        else {
            h['percentage'] = parseFloat(h['percentage']);
        }
        h['price'] = parseFloat(h['price']);
        delete h.remove;
        data.push(h);
    });

    // Output the result
    $EXPORT.text(JSON.stringify(data));

    let url = '/alerts/add_alerts/';
    let method = 'POST';

    helperMethods.secureHTTPRequestHandler(url, method, data, function (response) {
        $("#sideModalTR").on("shown.bs.modal", function () {  //Tell what to do on modal open
             $(this).find('#myModalLabel').html('Voila!!');
             $(this).find('.modal-body').html('Alert added successfully.');
        }).modal('show');

    }, function (response, status, error) {
        $("#sideModalTR").on("shown.bs.modal", function () {  //Tell what to do on modal open
             $(this).find('#myModalLabel').html('Oops!!');
             $(this).find('.modal-body').html(response.message);
        }).modal('show');
    })


});
