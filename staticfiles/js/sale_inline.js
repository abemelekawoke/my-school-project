(function($) {
    $(document).ready(function() {
        function updatePrice(element) {
            var itemTypeId = $(element).val();
            var soldUnitPriceField = $(element).closest('tr').find('input[id$=sold_unit_price]');
            if (itemTypeId) {
                $.ajax({
                    url: '/admin/get-sold-unit-price/',
                    data: {
                        'item_type': itemTypeId
                    },
                    success: function(data) {
                        soldUnitPriceField.val(data.price);
                    }
                });
            }
        }

        $('form').on('change', 'select[id$=item_type]', function() {
            updatePrice(this);
        });

        // Trigger price update on page load for pre-filled forms
        $('select[id$=item_type]').each(function() {
            if ($(this).val()) {
                updatePrice(this);
            }
        });
    });
})(django.jQuery);
