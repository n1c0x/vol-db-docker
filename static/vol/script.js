$(function () {
	$('.management_links').tooltip()
})


$(function($, undefined) {

    "use strict";

    // When ready.
    $(function() {
        
        var $form = $( "#new_vol" );
        // var $input = $form.find( "input" );
        var $input = $form.find( ".durationpicker" );

        $input.on( "keyup", function( event ) {
            
            
            // When user select text in the document, also abort.
            var selection = window.getSelection().toString();
            if ( selection !== '' ) {
                return;
            }
            
            // When the arrow keys are pressed, abort.
            if ( $.inArray( event.keyCode, [38,40,37,39] ) !== -1 ) {
                return;
            }
            
            var $this = $(this);
            var input = $this.val();
                    input = input.replace(/[\W\s\._\-]+/g, '');
                
                var split = 2;
                var chunk = [];

                for (var i = 0, len = input.length; i < len; i += split) {
                    split = 2;
                    chunk.push( input.substr( i, split ) );
                }

                $this.val(function() {
                    return chunk.join(":").toUpperCase();
                });
        
        } );
        
        // https://webdesign.tutsplus.com/tutorials/auto-formatting-input-value--cms-26745
        
    });
})