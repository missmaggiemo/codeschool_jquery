jQuery(document).ready(function(){

  // highlight fields
  $("#filters").on("click", ".on-sale-button", function(){
    $(".tour").filter(".on-sale").toggleClass("highlight-yellow");
  });

  $("#filters").on("click", ".featured-button", function(){
    $(".tour").filter(".featured").toggleClass("highlight-blue");
  });


  $(".destination").on("click", "#info", function(event){
    event.preventDefault();
    $(this).hide().closest("li").find(".more-info").slideToggle();
  });

  $(".guided-tour").on("click", "button", function(event){
    event.preventDefault();
    $(this).hide().closest("div").find("#price").fadeIn();
  });
  

});
