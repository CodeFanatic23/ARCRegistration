 $(document).ready(function(){
      $('select').select2();
    });
$(document).ready(function() {
    $('#add_form').submit(function() { // catch the form's submit event
        $.ajax({ // create an AJAX call...
            data: $(this).serialize(),// get the form data
            type: $(this).attr('method'), // GET or POST
            dataType: 'json',
            url: '/add/', // the file to call
            success: function(data) { // on success..
                 $('#add_form').closest('form').find("input[type=number], numberinput").val("");
                showLoading();
    setTimeout(function () {
        hideLoading();
        showDialog({
                        title: 'Status',
                        text: data.add_status
                    });
    }, 3000);
                    
    
            },
            error: function(e) { // on error..
                $('#err').html(e); // update the DIV
                // window.location.reload(true);
            }
        });
        
        return false;
    });
});

$(document).ready(function() {
    $('#remove_form').submit(function() { // catch the form's submit event
        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: '/remove/', // the file to call
            success: function(data) { // on success..
                $('#remove_form').closest('form').find("input[type=number], numberinput").val("");
                 showLoading();
                setTimeout(function () {
                    hideLoading();
                    showDialog({
                            title: 'Status',
                            text: data.remove_status
                        });
                    $.ajax({ // create an AJAX call...
            
                        type: 'GET', // GET or POST
                        url: '/home/', // the file to call
                        success: function(data) { // on success..
                            
                        },
                        error: function(e, x, r) { // on error..
                                    }
                    });
                }, 3000);
            },
            error: function(e, x, r) { // on error..
              window.location.reload(true);
                           }
        });
      return false;
    });
});



$(document).ready(function() {
$('.sub').click(function () {
    showDialog({
        title: 'Action',
        text: "Submit? There's no going back!",
        negative: {
            title: 'Nope'
        },
        positive: {
            title: 'Yay',
            onClick: function (e) {
                        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: '/submit/', // the file to call
            success: function(response) { // on success..
              window.location.reload(true);
                
            },
            error: function(e, x, r) { // on error..
            window.location.reload(true); 
            }
        });
            }
        }
    });
});

});

$(document).ready(function(){
    $("#add_button").click(function(){
        $("#show_add").slideToggle();
        $('html, body').animate({
                    scrollTop: $("#show_add").offset().top
                }, 500);
    });
});
$(document).ready(function(){
    $("#remove_button").click(function(){
        $("#show_remove").slideToggle();
        $('html, body').animate({
                    scrollTop: $("#show_remove").offset().top
                }, 500);
    });
});

$(document).ready(function(){
    console.log("hiding");
    $("#show_remove").hide();
    $("#show_add").hide(); 
});
