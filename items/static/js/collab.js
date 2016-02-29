// Our logic to grab the data from our profile
// edit form and submit via AJAX
function upload(event) {
    event.preventDefault();
    var data = new FormData($('form').get(0));

    $.ajax({
        url: $(this).attr('action'),
        type: $(this).attr('method'),
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: function(data) {
            // TODO: we shold look for errors and make
            // the status messages a little more robust
            // ad helpful when things go wrong

            if ('pic_url' in data) {
                $('img').attr('src', data.pic_url);
                $('.pic-status').show();
            } else {
                $('.name-status').show();

            }
        }
    });
    return false;
}

// Bind the form to JS function that will
// submit the form's data in an AJAX fasion
$( "form" ).submit(upload);


// When the user attached a new profile pic, submit
// the form
$(function() {
     $("input:file").change(function (){
       $('form').submit();
     });
  });


$( ".collaborator img" ).click(function() {
    $( ".upload-pic-button" ).click();
});

$("input:submit").click(function() {
    $('.bookmarklet-install-button').show();
});