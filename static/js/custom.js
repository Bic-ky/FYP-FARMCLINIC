
$(document).ready(function() {
    // add to cart
    $('.add_to_cart').on('click', function(e) {
        e.preventDefault();

        project_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response) {
                console.log(response);
                if (response.status == 'login_required') {
                    swal(response.message, '', 'info').then(function() {
                        window.location = '/account/login/';
                    });
                } else if (response.status == 'Failed') {
                    swal(response.message, '', 'error');
                } else if (response.status == 'Success') {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-' + project_id).html(response.qty);

                    // subtotal, tax, and grand total
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['grand_total']
                    );
                }
            },
            error: function(xhr, status, error) {
                var response = xhr.responseJSON;
                if (response.status == 'Failed' && response.message == 'Maximum share limit reached for this project!') {
                    swal({
                        title: 'Maximum Share Limit Reached',
                        text: 'You have reached the maximum share limit for this project.',
                        icon: 'warning',
                        button: 'OK'
                    });
                } else if (response.status == 'Failed' && response.message == 'Quantity exceeds the available share') {
                    swal({
                        title: 'Quantity Exceeds Available Share',
                        text: 'The available share limit for this project has been reached.',
                        icon: 'warning',
                        button: 'OK'
                    });
                } else {
                    alert('Error: ' + response.message);
                }
            }
        });
    });

    // place the cart item quantity on load
    $('.item_qty').each(function() {
        var the_id = $(this).attr('id');
        var qty = $(this).attr('data-qty');
        $('#' + the_id).html(qty);
    });

    // decrease cart
    $('.decrease_cart').on('click', function(e) {
        e.preventDefault();

        project_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id');

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response) {
                console.log(response)
                if (response.status == 'login_required') {
                    swal(response.message, '', 'info').then(function() {
                        window.location.href = '/account/login';
                    })
                } else if (response.status == 'Failed') {
                    swal(response.message, '', 'error')
                } else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-' + project_id).html(response.qty);

                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['grand_total']
                    );

                    if (window.location.pathname == '/cart/') {
                        removeCartItem(response.qty, cart_id);
                        checkEmptyCart();
                    }
                }
            }
        });
    });

    // DELETE CART ITEM
    $('.delete_cart').on('click', function(e) {
        e.preventDefault();

        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response) {
                console.log(response)
                if (response.status == 'Failed') {
                    swal(response.message, '', 'error')
                } else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    swal(response.status, response.message, "success")

                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['grand_total']
                    );

                    removeCartItem(0, cart_id);
                    checkEmptyCart();
                }
            }
        });
    });

    // delete the cart element if the qty is 0
    function removeCartItem(cartItemQty, cart_id) {
        if (cartItemQty <= 0) {
            // remove the cart item element
            $("#cart-item-" + cart_id).remove();
        }
    }

    // Check if the cart is empty
    function checkEmptyCart() {
        var cart_counter = parseInt($('#cart_counter').html());
        if (cart_counter === 0) {
            $("#empty-cart").css("display", "block");
        }
    }

    // apply cart amounts
    function applyCartAmounts(subtotal, tax_dict, grand_total) {
        if (window.location.pathname === '/ecom/cart/') {
            // Update the cart amounts on the '/ecom/cart/' page
            $('#subtotal').html(subtotal);
            $('#total').html(grand_total);
            
            console.log(tax_dict)
            for (key1 in tax_dict) {
                console.log(tax_dict[key1])
                for (key2 in tax_dict[key1]) {
                    // console.log(tax_dict[key1][key2])
                    $('#tax-' + key1).html(tax_dict[key1][key2]);
                }
            }
        }
    }
});

// GOOGLE API PART
let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['np']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }

    
    console.log(place);
    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_address').value

    geocoder.geocode({'address': address}, function(results, status){
        // console.log('results=>', results)
        // console.log('status=>', status)
        if(status == google.maps.GeocoderStatus.OK){
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

            // console.log('lat=>', latitude);
            // console.log('long=>', longitude);
            $('#id_latitude').val(latitude);
            $('#id_longitude').val(longitude);

            $('#id_address').val(address);
        }
    });

    // loop through the address components and assign other address data
    console.log(place.address_components);
    for(var i=0; i<place.address_components.length; i++){
        for(var j=0; j<place.address_components[i].types.length; j++){
            // get country
            if(place.address_components[i].types[j] == 'country'){
                $('#id_country').val(place.address_components[i].long_name);
            }
            // get state
            if(place.address_components[i].types[j] == 'administrative_area_level_1'){
                $('#id_state').val(place.address_components[i].long_name);
            }
            // get city
            if(place.address_components[i].types[j] == 'locality'){
                $('#id_city').val(place.address_components[i].long_name);
            }
            // get pincode
            if(place.address_components[i].types[j] == 'postal_code'){
                $('#id_pin_code').val(place.address_components[i].long_name);
            }else{
                $('#id_pin_code').val("");
            }
        }
    }

}
/* --------------------------------------------------------
        Status Update Modal
    -------------------------------------------------------- */

    $(document).ready(function() {
      // Event listener for the update status button
      $('.update_status_button').click(function() {
        var projectId = $(this).data('project-id');
        var projectTitle = $(this).data('project-title');
  
        // Set the project title in the modal
        $('#projectTitle').text(projectTitle);
  
        // Set the project ID as a data attribute in the form
        $('#statusForm').data('project-id', projectId);
  
        // Display the modal
        $('#myModal').css('display', 'block');
      });
  
      // Event listener for the close button
      $('#closeModal').click(function() {
        // Hide the modal
        $('#myModal').css('display', 'none');
      });
  
      // Event listener for the form submission
      $('#statusForm').submit(function(event) {
        event.preventDefault(); // Prevent the default form submission
  
        // Get the form action URL
        var formAction = $(this).attr('action');
  
        // Get the CSRF token
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
  
        // Get the project ID from the data attribute in the form
        var projectId = $(this).data('project-id');
  
        // Get the status from the textarea field
        var status = $('#statusForm textarea[name="status"]').val();
  
        // Create the form data object
        var formData = new FormData();
        formData.append('csrfmiddlewaretoken', csrfToken);
        formData.append('project_id', projectId);
        formData.append('status', status);
  
        // Perform the AJAX request
        $.ajax({
          url: formAction,
          method: 'POST',
          data: formData,
          processData: false,
          contentType: false,
          success: function(response) {
            console.log(response); // Display the response in the console
            if (response.message) {
              alert(response.message); // Show a success message
              $('#myModal').css('display', 'none'); // Close the modal
            } else if (response.error) {
              alert(response.error); // Show an error message
            }
          },
          error: function(xhr, status, error) {
            console.log(xhr.responseText); // Display the error in the console
            alert('An error occurred. Please try again.'); // Show a generic error message
          }
        });
      });
    });
 
/* --------------------------------------------------------
        Status VIEW
    -------------------------------------------------------- */

    
    









  