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
                $('#status').css({'background-color':'#ffbcbc','border':'1px dotted black','color':'black','border-radius':'3px','text-align':'center'});
                $('#status').html(data.add_status); // update the DIV
                $('#add_form').closest('form').find("input[type=number], numberinput").val("");
                $('html, body').animate({
                    scrollTop: $("#status").offset().top
                }, 500);
                //$('#status').delay(5000).fadeOut(400);
    
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
                 $('#status').css({'background-color':'#ffbcbc','border':'1px dotted black','color':'black','border-radius':'3px','text-align':'center'});
                 $('#status').html(data.remove_status); // update the DIV
                 $('html, body').animate({
                    scrollTop: $("#status").offset().top
                }, 500);
                //$('#status').delay(5000).fadeOut(400);
		$.ajax({ // create an AJAX call...
            
            type: 'GET', // GET or POST
            url: '/home/', // the file to call
            success: function(data) { // on success..
                
            },
            error: function(e, x, r) { // on error..
                           }
        });
            },
            error: function(e, x, r) { // on error..
              window.location.reload(true);
                           }
        });
      return false;
    });
});



$(document).ready(function() {
    $('#sub').click(function() { // catch the form's submit event
       var a = confirm("Submit? There's no going back!");
  if(a == true)
{
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
        return false;
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
