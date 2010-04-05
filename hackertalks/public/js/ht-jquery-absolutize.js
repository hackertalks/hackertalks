(function($){
	jQuery.fn.absolutize = function() {
        /*
         * original: http://blog.carbonfive.com/2008/09/javascript-ajax/absolutize-for-jquery
         * patched: element.offset() is page offset; what you want there is element.position()
         * remember:
         *      position: absolute is _relative_ to the nearest _positioned_ parent (read: position != static)
         * 
         * license:
         *      public domain // WTFPL
         */
        return this.each(function() {
            var element = $(this);
            if (element.css('position') == 'absolute')
            {
                return element;
            }
         
            var offsets = element.position();
            var top = offsets.top;
            var left = offsets.left;
            var width = element[0].clientWidth;
            var height = element[0].clientHeight;
         
            element._originalLeft = left - parseFloat(element.css("left") || 0);
            element._originalTop = top - parseFloat(element.css("top") || 0);
            element._originalWidth = element.css("width");
            element._originalHeight = element.css("height");
         
            element.css("position", "absolute");
            element.css("top", top + 'px');
            element.css("left", left + 'px');
            element.css("width", width + 'px');
            element.css("height", height + 'px');
            return element;
        });
	};

    /*
     * absolutize and insert a relatively-positioned replacement div to keep the layout intact.
     * works for low values of "intact" and most values of "layout"
     */
    jQuery.fn.absolutize_keeplayout = function() {
        return this.each(function() {
            var element = $(this);
            if (element.css('position') == 'absolute') {
                return element;
            }

            var new_e = document.createElement('div');
            if(element.attr('id'))
                new_e.id = element.attr('id')+'_replacement';
            new_e.style.width = element[0].style.width;
            new_e.style.height = element.css('height');
                                /* content does not get copied;
                                 * so fake it by applying current height */
            new_e.style.position = 'relative';
            new_e.style['float'] = element.css('float');
            new_e.style.clear = element.css('clear');
            new_e.style.margin = element.css('margin');
            new_e.style.padding = element.css('padding');
            
            element.absolutize();

            element.parent().append(new_e);
            console.log('inserted');
            return element;
        });
    };
})(jQuery);
