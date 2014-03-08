jQuery(document).ready(function(){

  $(".ajax-div").on("click", ".view-boarding-pass",function(event){
    event.preventDefault();
    console.log("view boarding pass");
    $(this).closest(".flight").find(".ticket").slideToggle();
  });

  $('form[id=check-flights]').on('submit', function(event) {
    var form = $(this);
    console.log(form);
    var data = form.serialize();
    event.preventDefault();
    $.ajax(form.attr('action'), {
      type: 'POST',
      data: data,
      success: function(result) {
        console.log(result);
        form.closest("body").find(".ajax-div").html(result).fadeIn();
      }
    });
  });

});
