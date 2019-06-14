$(function() {
    console.log('Autofill running');
    $("#singleColourNameField").autocomplete({
        source: function (request, response) {
            console.log('Getting JSON')
            $.getJSON("/autocomplete-colour", {   // Requests a JSON payload from /autocomplete-colour
                q: request.term, // Refer to my routes.py
            }, function (data) {
                if(data.matching_results.length >= 1) {
                    document.getElementById('singleColourNameField').style.background = "pink";
                    response(data.matching_results);
                    // This highlights the field
                }
                else{
                    document.getElementById('singleColourNameField').style.background = "#42f4a7"
                }
            });
        },
        minLength: 2,
        select: function (event, ui) {
            console.log(ui.item.value); //
        }
    });
})
