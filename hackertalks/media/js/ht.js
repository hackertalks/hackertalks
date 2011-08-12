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

var just_changedlights=false;

var lights = {
    'on': function() {
        document.body.className='';
        $('.overlay').animate({opacity: 0}, 1000, function() { $('.overlay').remove(); });
        just_changedlights=true;
    },
    'out': function() {
        $('#talk_container').absolutize_keeplayout();
        $('#talk_container').css('z-index', 100);
        if($('#talk_container').css('background-image')) {
            $('#talk_container_replacement').css('background-image', $('#talk_container').css('background-image'));
            $('#talk_container_replacement').css('background-repeat', $('#talk_container').css('background-repeat'));
            $('#talk_container_replacement').css('background-position', $('#talk_container').css('background-position'));
            $('#talk_container').css('background', 'none');
        }
        var e = document.createElement('div');
        e.style.height='100%';
        e.style.width='100%';
        e.style.zIndex='99';
        e.style.position='absolute';
        e.style['top']=0;
        e.style.left=0;
        e.className = 'overlay';
        e.style.backgroundColor='black';
        e.style.opacity=0;
        $(e).animate({opacity: 1});
        document.body.className='lightsoff';
        document.body.appendChild(e);
        just_changedlights=true;
    },
    'toggle': function() {
        if(document.body.className=='lightsoff')
            lights.on();
        else
            lights.out();
    }
};

var current_second = 0;
var getUpdate = function(type,arg1,arg2) {
    if(type=='time') {
        if(just_changedlights && current_second > arg1) {
            var current_second_gah = current_second;

            setTimeout(function() { $('#talk_container embed')[0].sendEvent('play'); }, 2000);
            setTimeout(function() { $('#talk_container embed')[0].sendEvent('scrub', current_second_gah); }, 3000);
        }
        just_changedlights=false;
        current_second = arg1;
    }
};
