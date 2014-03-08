// destination and tour script

jQuery(document).ready(function(){

  // update price
  $("form #num-people").on("keyup", function() {
    var num_people = $(this).val();
    var price_per_person = $(this).closest(".flight-form").data("price");
    $(this).closest("form").find("#price-input").val(num_people * price_per_person);
    $(this).closest("form").find("#price-total").text(num_people * price_per_person);
  });

});
