$(function() {
    $("#stumble_duration").slider({range: true,
                                   min: 0,
                                   max: 90,
                                   values:[$('[name=duration_start]')[0].value,
                                           $('[name=duration_end]')[0].value],
                                   slide: function(event, ui) {
                                    $('[name=duration_start]')[0].value = ui.values[0];
                                    $('[name=duration_end]')[0].value = ui.values[1];
                                    $('#duration_start_display').html(ui.values[0]);
                                    $('#duration_end_display').html(ui.values[1]);
                                   }
                                 });
    $('#duration_start_display').html($('[name=duration_start]')[0].value);
    $('#duration_end_display').html($('[name=duration_end]')[0].value);
});
