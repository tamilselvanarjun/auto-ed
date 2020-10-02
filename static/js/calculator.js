$(document).ready(function() {
    // when add form is submitted



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
                // update display function
                $(`input[type=text][name=f${data.editing+1}]`).attr('value',`${data.func_content[data.editing]}`);

            }

        });
        
      return false;

    });






});