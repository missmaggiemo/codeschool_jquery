// javascript scraps


// $.ajax with POST
$('form').on('submit', function(event) {
  var form = $(this);
  console.log(form);
  var data = $('form').serialize();
  if(form.find(".first-name").val() && form.find(".last-name").val()){
    console.log()
    event.preventDefault();
    $.ajax($('form').attr('action'), {
      type: 'POST',
      data: data,
      success: function(result) {
        console.log(result);
        form.parent().hide().html(result).fadeIn();
      }
    });
  }
});





// update nights
$(".tour #nights").on("keyup", function() {
  var night_count = $(this).val();
  var daily_price = $(this).closest(".tour").data("daily-price");
  $(this).closest(".tour").find("#nights-count").text(night_count);
  $(this).closest(".tour").find("#total").text(night_count * daily_price);
  $(this).closest("form").find("#totalPrice").val(night_count * daily_price);
});
$(".tour #nights").on("focus", function(){
  $(this).val(7);
});

// $.ajax with POST
$('form').on('submit', function(event) {
  event.preventDefault();
  var form = $(this);
  var data = form.serialize();
  $.ajax($('form').attr('action'), {
    type: 'POST',
    dataType: 'json',
    data: data,
    success: function(result) {
      console.log(result);
      var msg = $("<a href='" +result.link+ "'></a>");
      msg.append("Destination: " + result.destination + ". ");
      msg.append("Nights: " + result.nights + ". ");
      msg.append("Price: $" + result.totalPrice + ".");
      console.log(msg);
      form.closest(".vacation").hide().html(msg).fadeIn();
    }
  });
});



// toggle photos
$(".photo-holder-div").on("click", "a", function() {
  event.stopPropagation();
  event.preventDefault();
  $(".photos").slideToggle(400);
  $(this).parent().children("ul").addClass("margin");
});

// animate tour headings
// $(".tour h2").on("mouseenter", function() {
//   $(this).animate({"padding": "30px"}, 300);
// });
// $(".tour h2").on("mouseleave", function() {
//   $(this).animate({"padding": "20px"}, 300);
// });


// phone number
$(".tour").on("click", ".book", function(){
  var message = "Call 1-555-jquery-air to book this tour";
  $(this).closest("li").find("#phone-number").text(message);
  $(this).hide();
});
