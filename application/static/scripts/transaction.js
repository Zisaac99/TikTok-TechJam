$(document).ready(function () {
    var table = $('#myTable').DataTable({
            // Enable server-side processing 
            "serverSide": true,
            "ajax": {// Define the api for the server-side processing and also sends the status that is choosen in the dropdown
                "url": "/api/ssp_transaction"
            },// Data that is returned from the api and here we set which columns the data belongs to
            "columns": [
                { "data": "transaction_id" },
                { "data": "amount" },
                { "data": "type" },
                { "data": "date" },

            ]
        });
        
    setInterval(function () {//Every 5 seconds the table is refreshed by calling the ssp api
        table.ajax.reload(null, false);
    }, 5000);    
});