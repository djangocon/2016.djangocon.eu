$(function() {
    var emojiMode = false;
    function emojiModeOn() {
        emojiMode = true;
        $('[data-emoji-alt]').each(function() {
            $(this).attr('title', $(this).text()).text($(this).data('emoji-alt')).addClass('emoji-alt');
        });
    }
    function emojiModeOff() {
        emojiMode = false;
        $('.emoji-alt').each(function() {
            $(this).text($(this).attr('title')).removeAttr('title').removeClass('emoji-alt');
        });
    }
    $('.emojimode-toggler').click(
        function() {
            if(emojiMode){
                emojiModeOff();
                $(this).attr('title', 'Turn on emoji mode').text('😺');
            }
            else {
                emojiModeOn();
                $(this).attr('title', 'Turn off emoji mode').text('😿');
            }
        }
    );

    var bulbs = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1];
    var footer = $('footer');
    var fakeimg = $('<div class="fakeimg">');
    footer.prepend(fakeimg);
    footer.addClass('jsified');

    $.each(bulbs, function(index){
        var bulb = $('<span class="bulb">');
        if (!bulbs[index]) {
            bulb.addClass('off');
        }
        var offset = 56 + index * 40;
        bulb.css('left', offset);
        bulb.click(function(){$(this).toggleClass('off'); checkBulbs(fakeimg);});
        fakeimg.append(bulb);
    });
});

$(function() {
    var currentDate = new Date();
    if((currentDate.getMinutes() == 42) && (currentDate.getSeconds() % 10 == 0)) {
        $('.emojimode-toggler').click();
    }
});

if (window.addEventListener && window.wrmqrm) {
  var state = 0, keyseq = [38,38,40,40,37,39,37,39,66,65];
  window.addEventListener("keydown", function(e) {
    if (e.keyCode == keyseq[state]){
        state++;
    }
    else {
        state = 0;
    }
    if (state == keyseq.length) {
        $('img.speakerpicture').attr('src', window.wrmqrm['img']);
        new Audio(window.wrmqrm['audio']).play();
    }
    }, true);
}

function checkBulbs(container) {
    if(window.wompwomp && $('.bulb', container).not('.off').length == 0) {
        new Audio(window.wompwomp).play();
    }
}
