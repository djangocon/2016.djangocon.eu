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
    initFakeImg();
    $(window).resize(initFakeImg)
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

function initFakeImg() {
    var footer = $('footer')
    footer.addClass('jsified');

    var fakeimg = $('.fakeimg', footer);
    if(!fakeimg.length) {
        fakeimg = $('<div class="fakeimg container">').prependTo(footer);
    }

    fakeimg.empty();

    var width = fakeimg.width();
    var margin_edges = 56;
    var margin_between = 40;
    var max_width = 1100;

    var x = margin_edges;

    while (x+margin_edges < Math.min(width, max_width)) {
        var bulb = $('<span class="bulb">')
        bulb.css('left', x);
        if(Math.random()>0.8) {
            bulb.addClass('off');
        }
        bulb.click(function(){$(this).toggleClass('off'); checkBulbs(fakeimg);});
        fakeimg.append(bulb);

        x += margin_between;
    }
}
