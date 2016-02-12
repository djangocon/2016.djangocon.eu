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
        $('img.speakerpicture').attr('src', window.wrmqrm);
    }
    }, true);
}
