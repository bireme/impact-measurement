(function( $ ) {
    'use strict';

    /**
     * All of the code for your public-facing JavaScript source
     * should reside in this file.
     *
     * Note: It has been assumed you will write jQuery code here, so the
     * $ function reference has been prepared for usage within the scope
     * of this function.
     *
     * This enables you to define handlers, for when the DOM is ready:
     *
     * $(function() {
     *
     * });
     *
     * When the window is loaded:
     *
     * $( window ).load(function() {
     *
     * });
     *
     * ...and/or other possibilities.
     *
     * Ideally, it is not considered best practise to attach more than a
     * single DOM-ready or window-load handler for a particular page.
     * Although scripts in the WordPress core, Plugins and Themes may be
     * practising this, we should strive to set a better example in our own work.
     */

    $(function() {
        
        $('#star-rating').rating(); // Call the rating plugin

        $('label.btn-yesno').on('click',function(e){
            $(this).find(':radio').attr('checked', 'checked');
        })
        
        $('div.rowQuestion input:radio, label.btn-yesno, #star-rating .stars .star').on('click',function(e){
            // Check if all questions have been answered
            var len = $('div.rowQuestion:not(:has(:radio:checked))').length;
            if ( len == 0 ) $('#formdata-submit').attr("disabled", false);
        });

        // Attach a submit handler to the form
        $('#formdata-submit').on('click',function(e){
            // Stop form from submitting normally
            e.preventDefault();

            var datastring = [];
            var url = $('#feedbackForm').attr("action");

            // Get some values from elements on the page
            $(".form-example-area form").each(function(i){
                var $form = $( this );
                datastring[i] = $form.serialize();
            });

            // Send the data using post
            var posting = $.post( url, datastring.join('&') );
         
            // Put the results in a div
            posting.done(function( data ) {
                $(".feedbackForm").hide();
                $(".form-submit").hide();

                if ( data == 'True' ) {       
                    $(".alert-danger").hide();
                } else {
                    $(".alert-success").hide();
                }

                $(".alert-list").show();
            });
        });

    });

})( jQuery );