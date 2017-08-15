$(document).ready(function() {
  $('.collapsible').collapsible();
  $('#add-observation-btn').click(function() {
    observations.initNew();
  })
});

$newObservationWrapper = $('#new-observation');
$drawingForm = $( '#drawing-form' );

var observations = {
  startNew: function() {
    $('#stepone').removeClass('visible');
    $('#steptwo').addClass('visible');
    $('#use-my-location').click(function() {
      findLocation();
      observations.stepTwo();
    });
    $('#choose-from-map').click(function() {
      drawLocation();
      observations.stepTwo();
    })
  },
  stepTwo: function() {
    $('#steptwo').removeClass('visible');
    $('#stepthree').addClass('visible');
    $newObservationWrapper.addClass('short');
    $('#loc-correct').click(function() {
      $('#stepthree').removeClass('visible');
      $('#stepfour').addClass('visible');
      $newObservationWrapper.removeClass('short');
      $newObservationWrapper.addClass('tall');
    });
  },
  close: function() {
    $newObservationWrapper.find('form').html('');
    $newObservationWrapper.removeClass('visible tall');
  },
  showSpinner: function() {
    $('.preloader-wrapper').addClass('active');
  },
  hideSpinner: function() {
    $('.preloader-wrapper').removeClass('active');
  },
  initNew: function() {
    $newObservationWrapper
    $newObservationWrapper.toggleClass('visible');
    if (!$newObservationWrapper.hasClass('visible')) {
      $drawingForm.html('');
      return;
    }
    return $.ajax({
        url: '/observation/new/',
        success: function(data) {
            $drawingForm.html(data);
        },
        error: function (result) {
            //debugger;
        }
    }).done(function() {
      $('.timepicker').pickatime({
        default: 'now', // Set default time: 'now', '1:30AM', '16:30'
        fromnow: 0,       // set default time to * milliseconds from now (using with default = 'now')
        donetext: 'Okay', // text for done-button
        cleartext: 'Clear', // text for clear-button
        autoclose: false, // automatic close timepicker
        aftershow: function(){} //Function for after opening timepicker
      });
      $('.datepicker').pickadate({
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 5,
        today: 'Today',
        clear: 'Clear',
        close: 'Ok',
        closeOnSelect: false // Close upon selecting a date,
      });
      $drawingForm.submit(function(e) {
        e.preventDefault();
        observations.create(e.target);
        observations.close();
        let stopTracking = true;
        findLocation(stopTracking);
      })
    });
  },
  create: function(form) {
    $form = $(form).serialize();
    return $.ajax({
      type: 'POST',
      url: '/observation/create/',
      data: $form,
      success: function(data) {
        $drawingForm.html('');
      },
      error: function (error) {
        $drawingForm.prepend(error);
      }
    });
  }
};
