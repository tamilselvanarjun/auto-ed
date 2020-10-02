$(document).ready(function() {
    // when add form is submitted


    // when calculator buttons are pressed (except Calculate & Clear Function)
    $(document).on('submit', 'form[name="calculator"]', function(event) {
        // prevent POST request from refreshing
        event.preventDefault();

        // select which button was triggered
        var $btn = $(document.activeElement);

        // send ajax request
        $.ajax({
            type:'POST',
            url:"press-calculator",
            data:{
                action: $btn.val(),
            },

            // when ajax request is successful
            success:function(data) {
                // update button style if "Edit F" button is pressed
                if ($btn.val() == 'Edit f1') {
                    $('input[type=text][name="f1"]').css('background-color','#87ceeb');
                    $('input[type=text][name="f2"]').css('background-color', 'white');
                    $('input[type=text][name="f3"]').css('background-color', 'white');
                }

                else if($btn.val() == 'Edit f2') {
                    $('input[type=text][name="f2"]').css('background-color','#87ceeb');
                    $('input[type=text][name="f1"]').css('background-color', 'white');
                    $('input[type=text][name="f3"]').css('background-color', 'white');
                }

                else if($btn.val() == 'Edit f3') {
                    $('input[type=text][name="f3"]').css('background-color','#87ceeb');
                    $('input[type=text][name="f2"]').css('background-color', 'white');
                    $('input[type=text][name="f1"]').css('background-color', 'white');
                };

                // update display function
                $(`input[type=text][name=f${data.editing+1}]`).attr('value',`${data.func_content[data.editing]}`);

            }

        });
        
      return false;

    });


    


    // when 'Clear Function' pressed
    $(document).on('submit', 'form[name="clear-function"]', function(event) {
        // prevent POST request from refreshing
        event.preventDefault();

        // send ajax request
        $.ajax({
            type:'POST',
            url:"clear-function-calculator",
            data:{
                action: "Clear Function",
            },

            // when ajax request is successful
            success:function(data) {
                // update display function
                $(`input[type=text][name=f${data.editing+1}]`).attr('value',`${data.func_content[data.editing]}`);

            }

        });
        
      return false;

    });





});