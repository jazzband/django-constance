(function($) {
    'use strict';

    $(function() {
        $('#content-main').on('click', '.reset-link', function(e) {
            e.preventDefault();

            var field = $('#' + this.dataset.fieldId);

            if (field.attr('type') === 'checkbox') {
                field.prop('checked', this.dataset.default === 'true');
            } else {
                field.val(this.dataset.default);
            }
        });
    });
})(django.jQuery);
