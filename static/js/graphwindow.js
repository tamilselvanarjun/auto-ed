// MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}});


// for web compatibility: chrome and edge already works, and with this code firefox and safari will also work.  
// help from: https://zellwk.com/blog/inconsistent-button-behavior/
document.addEventListener('click', function (event) {
    if (event.target.matches('input')) {
      event.target.focus()
    }
    else if (event.target.matches('button')) {
        event.target.focus()
      }
  })


$(document).ready(function() {

    // when function to visualize is selected
    $(document).on('submit', 'form[name="select-func-viz"]', function(event) {
        // prevent POST request from refreshing
        event.preventDefault();

        // select which function button was triggered
        var $btn = $(document.activeElement);

        // send ajax request
        $.ajax({
            type:'POST',
            url:"select-func-viz",
            data:{
                action: $btn.val(),
            },

            // when ajax request is successful
            success:function(data) {


                // highlight selected function
                $('.active', 'form[name="select-func-viz"]').removeClass('active');
                $btn.addClass('active');


                // if selected function is a constant, provide error
                if (data.is_constant[data.visfunc] == 1) {
                    alert("The function you've selected is a constant. The graph and derivative are trivial so are not displayed here.");
                    // hide graphbox display
                    $('#graphbox').addClass('hidden');
                    return;
                }
            

                /* update contents in graphbox */
                
                //update computational graph
                var compGraph = document.createElement('img');
                compGraph.src = "data:image/svg+xml;base64," + data.comp_graph;
                compGraph.alt = 'computational graph'
                $('#computational-graph').empty().append(compGraph);
                $('#computational-graph').append('<br><br>');

                // update evaluation table
                $('#evaluation-table').empty().append(data.table);

                // update reverse graph
                var revGraph = document.createElement('img');
                revGraph.src = "data:image/svg+xml;base64," + data.rev_graph;
                revGraph.alt = 'reverse graph'
                $('#reverse-graph').empty().append(revGraph);
                $('#reverse-graph').append('<br><br>');

                // update dynamic reverse graph
                var revDynamic = document.createElement('img');
                revDynamic.src = "data:image/svg+xml;base64," + data.rev_dynamic_graph;
                revDynamic.alt = 'dynvis'
                $('#reverse-dynamic').empty().append(revDynamic);
            
                
                // appropriately refresh partial derivative buttons
                $('form[name="partial-der"]').empty();
                
                var partialDerButtons = document.createElement('p');

                if(data.visfunc == 0) {
                    partialDerButtons.innerHTML += ('<button id="derbutton" class="btn btn-outline-info" type="submit" name="action" value="dyn00">df1/dx0</button> &nbsp;');    
                    if(data.ins > 1) {
                        partialDerButtons.innerHTML += ('<button id="derbutton" class="btn btn-outline-info" type="submit" name="action" value="dyn01">df1/dx1</button> &nbsp;');
                    }
                    if(data.ins > 2) {
                        partialDerButtons.innerHTML += ('<button id="derbutton" class="btn btn-outline-info" type="submit" name="action" value="dyn02">df1/dx2</button> &nbsp;');
                    }                    
                    if(data.ins > 3) {
                        partialDerButtons.innerHTML += ('<button id="derbutton" class="btn btn-outline-info" type="submit" name="action" value="dyn03">df1/dx3</button> &nbsp;');
                    }
                    if(data.ins > 4) {
                        partialDerButtons.innerHTML += ('<button id="derbutton" class="btn btn-outline-info" type="submit" name="action" value="dyn04">df1/dx4</button>');
                    }
                };

                if(data.visfunc == 1) {
                    partialDerButtons.innerHTML += ('<button id="derbutton" class="btn btn-outline-info" type="submit" name="action" value="dyn10">df2/dx0</button> &nbsp;');    
                    if(data.ins > 1) {
                        partialDerButtons.innerHTML += ('<button id="derbutton" class="btn btn-outline-info" type="submit" name="action" value="dyn11">df2/dx1</button> &nbsp;');
                    }
                    if(data.ins > 2) {
                        partialDerButtons.innerHTML += ('<button id="derbutton" class="btn btn-outline-info" type="submit" name="action" value="dyn12">df2/dx2</button> &nbsp;');
                    }                    
                    if(data.ins > 3) {
                        partialDerButtons.innerHTML += ('<button id="derbutton" class="btn btn-outline-info" type="submit" name="action" value="dyn13">df2/dx3</button> &nbsp;');
                    }
                    if(data.ins > 4) {
                        partialDerButtons.innerHTML += ('<button id="derbutton" class="btn btn-outline-info" type="submit" name="action" value="dyn14">df2/dx4</button>');
                    }
                };


                if(data.visfunc == 2) {
                    partialDerButtons.innerHTML += ('<button id="derbutton" class="btn btn-outline-info" type="submit" name="action" value="dyn20">df3/dx0</button> &nbsp;');    
                    if(data.ins > 1) {
                        partialDerButtons.innerHTML += ('<button id="derbutton" class="btn btn-outline-info" type="submit" name="action" value="dyn21">df3/dx1</button> &nbsp;');
                    }
                    if(data.ins > 2) {
                        partialDerButtons.innerHTML += ('<button id="derbutton" class="btn btn-outline-info" type="submit" name="action" value="dyn22">df3/dx2</button> &nbsp;');
                    }                    
                    if(data.ins > 3) {
                        partialDerButtons.innerHTML += ('<button id="derbutton" class="btn btn-outline-info" type="submit" name="action" value="dyn23">df3/dx3</button> &nbsp;');
                    }
                    if(data.ins > 4) {
                        partialDerButtons.innerHTML += ('<button id="derbutton" class="btn btn-outline-info" type="submit" name="action" value="dyn24">df3/dx4</button> &nbsp;');
                    }
                };

                

                $('form[name="partial-der"]').append(partialDerButtons);
                // MathJax.Hub.Queue(["Typeset", MathJax.Hub, "myDiv"]);
                
                // hide prev/next buttons if they exist 
                $('form[name="navigate-steps"]').empty();
                
                // display graphbox
                $('#graphbox').removeClass('hidden');

            },
            error:function() {
                alert("Your session has expired, please start again from homepage.")
            }

        });
        
      return false;

    });


    // when partial derivative is selected
    $(document).on('submit', 'form[name="partial-der"]', function(event) {
        // prevent POST request from refreshing
        event.preventDefault();

        // select which function button was triggered
        var $btn = $(document.activeElement);
        console.log($btn.val())

        // send ajax request
        $.ajax({
            type:'POST',
            url:"partial-der",
            data:{
                action: $btn.val(),
            },

            // when ajax request is successful
            success:function(data) {

                // highlight selected partial derivative
                $('.active', 'form[name="partial-der"]').removeClass('active');
                $btn.addClass('active');


                // update dynamic reverse graph
                var revDynamic = document.createElement('img');
                revDynamic.src = "data:image/svg+xml;base64," + data.rev_dynamic_graph;
                revDynamic.alt = 'dynvis'
                $('#reverse-dynamic').empty().append(revDynamic);

                // add previous and next step buttons
                $('form[name="navigate-steps"]').empty();

                var navigateButtons = document.createElement('p');
                navigateButtons.innerHTML+= '<br>';


                navigateButtons.innerHTML += ('<button id="textbutton" class="btn btn-danger" type="submit" name="action" value="prev" disabled>Previous Step</button> &nbsp;'); 
                if(data.no_steps == true) { // if function is simple so there is only one step, disable both prev/next buttons
                    navigateButtons.innerHTML += ('<button id="textbutton" class="btn btn-success" type="submit" name="action" value="next" disabled>Next Step</button>'); 
                } else {
                    navigateButtons.innerHTML += ('<button id="textbutton" class="btn btn-success" type="submit" name="action" value="next">Next Step</button>');
                }
                 
            
                $('form[name="navigate-steps"]').append(navigateButtons);

            },
            // when ajax request is not successful
            error:function() {
                alert("Visualization not available. This happens when: (1) the computational graph of the function consists of only one node, (2) the function does not have any dependence on the selected input variable, or (3) your session expired (please start again from homepage).")
            }

        });
        
      return false;

    });

    // when user navigates visualization steps: Previous or Next
    $(document).on('submit', 'form[name="navigate-steps"]', function(event) {
        // prevent POST request from refreshing
        event.preventDefault();

        // select which function button was triggered
        var $btn = $(document.activeElement);
        console.log($btn.val())

        // send ajax request
        $.ajax({
            type:'POST',
            url:"navigate-steps",
            data:{
                action: $btn.val(),
            },

            // when ajax request is successful
            success:function(data) {

                // update dynamic reverse graph
                var revDynamic = document.createElement('img');
                revDynamic.src = "data:image/svg+xml;base64," + data.rev_dynamic_graph;
                revDynamic.alt = 'dynvis'
                $('#reverse-dynamic').empty().append(revDynamic);

                // disable buttons if not appropriate
                if(data.reached_max == true) { 
                    $('button[value="next"]').prop('disabled', true); // if reached final step, disable "next"
                } else {
                    $('button[value="next"]').prop('disabled', false);
                };

                if(data.curr_idx > 0) {
                    $('button[value="prev"]').prop('disabled', false);
                } else { 
                    $('button[value="prev"]').prop('disabled', true); // if back to first step, disable "previous"
                }

            },
            // when ajax request is not successful
            error:function() {
                alert("Your session has expired, please start again from homepage.")
            }

        });
        
      return false;

    });



});