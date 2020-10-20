
// for web compatibility: chrome and edge already works, and with this code firefox and safari will also work.  
// thanks to: https://zellwk.com/blog/inconsistent-button-behavior/
// document.addEventListener('click', function (event) {
//     if (event.target.matches('input')) {
//       event.target.focus()
//     }
//   })


$(document).ready(function() {
    // when add form is submitted

    // when calculator buttons are pressed (except Calculate & Clear Function)
    $(document).on('submit', 'form[name="calculator"]', function(event) {
        // prevent POST request from refreshing
        
        
        event.preventDefault();

        // select which button was triggered
        // Safari does not capture button's active element
        // https://stackoverflow.com/questions/46036196/document-activeelement-not-returning-the-active-element-in-safari
        var $btn = $(document.activeElement);
        console.log($btn);
        


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

            },
            error:function() {
                alert("Your session has expired, please start again from homepage.")
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

            },
            error:function() {
                alert("Your session has expired, please start again from homepage.")
            }

        });
        
      return false;

    });





});