function Confirmation(el) {
  var confirmation = this;
  
  console.log("variable 'confirmation':");
  console.log(confirmation);
  
  this.el = el;
  
  console.log("variable 'el':");
  console.log(el);
  
  this.flight = this.el.find(".flight");
  
  this.loadConfirmation = function(){ 
    $.ajax('/scripts/confirmation.html', {
      timeout: 3000,
      context: confirmation,
      success: function(response) {
        this.flight.html(response);
        this.flight.slideToggle();
      },
      error: function(request, errorType, errorMessage) {
        alert(request + '\nError: ' + errorType + ' with message: ' + errorMessage);
      }, 
      beforeSend: function(request) {
        
        console.log("ajax request start");
        console.log(request);
        
        $('.confirmation').addClass('is-loading'); 
      },
      complete: function() {
        console.log("ajax request finished");
        $('.confirmation').removeClass('is-loading');
      }
    });
  };
  this.showBoardingPass = function(event) {
    event.preventDefault();
    $(this).hide();
    confirmation.el.find(".boarding-pass").show();
  };
  
  this.el.on("click", "button", this.loadConfirmation);
  this.el.on("click", ".view-boarding-pass", this.showBoardingPass);
  
}

$(document).ready(function() {
  var paris = new Confirmation($('#paris'));
  var london = new Confirmation($('#london'));
});




