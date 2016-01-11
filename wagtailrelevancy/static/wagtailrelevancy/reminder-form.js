$(function() {
    buildExpandingFormset('id_reminder_set', {
        onInit: function(index) {
            var deleteInputId = 'id_reminder_set-' + index + '-DELETE';
            var childId = 'inline_child_reminder_set-' + index;
            $('#' + deleteInputId + '-button').click(function() {
                /* set 'deleted' form field to true */
                $('#' + deleteInputId).val('1');
                $('#' + childId).fadeOut();
            });
        }
    });
});
