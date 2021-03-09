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
        $(e.target).parent().parent().next().find('.answer-container').css(
            {
                "visibility": "visible",
                "height": "auto",
                "width": "auto"
            }
        )
    })
    $('.mark-answer').click(function (e) {
        e.preventDefault()
        $(e.target).parent().addClass('bg-success');

        payload = { 'a_id': $(e.target).prev().val() }
        $.post("/question/answer", payload, function (data) {
            console.log(data)
        });
    })



});