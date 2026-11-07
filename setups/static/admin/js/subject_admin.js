// static/admin/js/subject_admin.js
(function($) {
    'use strict';
    
    $(document).ready(function() {
        // 1. FUNCTION TO TOGGLE ALL CHECKBOXES
        function toggleAllGrades(isChecked) {
            $('.grade-level-checkboxes input[type="checkbox"]').prop('checked', isChecked);
        }
        
        // 2. SET UP SELECT ALL CHECKBOX
        $('#select_all_checkbox').change(function() {
            toggleAllGrades(this.checked);
        });
        
        // 3. MAKE THE LABEL CLICKABLE
        $('#select-all-label').click(function() {
            var checkbox = $('#select_all_checkbox');
            checkbox.prop('checked', !checkbox.prop('checked')).trigger('change');
        });
        
        // 4. UPDATE SELECT ALL WHEN INDIVIDUAL CHECKBOXES CHANGE
        function updateSelectAllCheckbox() {
            var total = $('.grade-level-checkboxes input[type="checkbox"]').length;
            var checked = $('.grade-level-checkboxes input[type="checkbox"]:checked').length;
            $('#select_all_checkbox').prop('checked', total === checked);
        }
        
        $('.grade-level-checkboxes').on('change', 'input[type="checkbox"]', updateSelectAllCheckbox);
        
        // 5. ORGANIZE CHECKBOXES INTO TWO ROWS
        function organizeCheckboxesIntoTwoRows() {
            var gradeCheckboxes = $('.grade-level-checkboxes');
            if (gradeCheckboxes.length) {
                // Get all list items
                var listItems = gradeCheckboxes.find('li');
                var totalItems = listItems.length;
                
                if (totalItems > 0) {
                    // Clear the container
                    gradeCheckboxes.empty();
                    
                    // Calculate how many items per row (split into 2 rows)
                    var itemsPerRow = Math.ceil(totalItems / 2);
                    
                    // Create first row container
                    var row1 = $('<div class="grade-row grade-row-1"></div>').css({
                        'display': 'grid',
                        'grid-template-columns': 'repeat(' + Math.min(itemsPerRow, 7) + ', 1fr)',
                        'gap': '5px 10px',
                        'margin-bottom': '10px'
                    });
                    
                    // Create second row container (if needed)
                    var row2 = $('<div class="grade-row grade-row-2"></div>').css({
                        'display': 'grid',
                        'grid-template-columns': 'repeat(' + Math.min(totalItems - itemsPerRow, 7) + ', 1fr)',
                        'gap': '5px 10px'
                    });
                    
                    // Distribute items into rows
                    listItems.each(function(index) {
                        $(this).css({
                            'margin': '0',
                            'padding': '2px 0',
                            'list-style': 'none'
                        });
                        
                        if (index < itemsPerRow) {
                            row1.append($(this));
                        } else {
                            row2.append($(this));
                        }
                    });
                    
                    // Add rows to container
                    gradeCheckboxes.append(row1);
                    if (row2.children().length > 0) {
                        gradeCheckboxes.append(row2);
                    }
                    
                    // Style the checkboxes inside
                    $('.grade-level-checkboxes label').css({
                        'display': 'flex',
                        'align-items': 'center',
                        'cursor': 'pointer',
                        'padding': '2px 5px',
                        'border-radius': '3px',
                        'white-space': 'nowrap'
                    });
                    
                    $('.grade-level-checkboxes label:hover').css({
                        'background-color': '#f5f5f5'
                    });
                    
                    $('.grade-level-checkboxes input[type="checkbox"]').css({
                        'margin-right': '8px'
                    });
                }
            }
        }
        
        // 6. INITIALIZE
        updateSelectAllCheckbox();
        organizeCheckboxesIntoTwoRows();
        
        // 7. REORGANIZE WHEN THE DOM CHANGES (for dynamic forms)
        $(document).on('formset:added', organizeCheckboxesIntoTwoRows);
    });
})(django.jQuery);