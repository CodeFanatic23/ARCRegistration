$(document).ready(function(){
  $("button").click(function(){
    $.ajax({
      url: "/add",
      context: document.body,
      success: function(response){
        $('p').html(response);
      }
    });
  });
});