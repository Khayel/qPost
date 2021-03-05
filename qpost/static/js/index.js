$(document).ready(() => {
    console.log("Ready");
    $('.q').click(() => {
        $('.new_question').css({
            "visibility": "visible",
            "height": "100vH",
            "width": "100vW"
        });


    })
    $('.new_question').click(function (e) {
        console.log(e.target)
        if (e.target !== this) {
            return;
        }

        $('.new_question').css({
            "visibility": "hidden",
            "height": "0vH",
            "width": "0vW"
        });
    })
    $('.answer-button').click(function (e) {
        e.preventDefault()
        console.log($(e.target).parent().next())
        $(e.target).parent().next().find('.answer-container').css(
            {
                "visibility": "visible",
                "height": "auto",
                "width": "auto"
            }
        )
    })



});