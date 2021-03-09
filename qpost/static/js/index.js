$(document).ready(() => {
    console.log("Ready");
    $('.q').click(() => {
        $('.new_question').css({
            "visibility": "visible",
            "height": "100vH",
            "width": "100vW"
        });


    })
    $('.new_question').on('click', function (e) {
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
    $('.answer-button').on('click', function (e) {
        e.preventDefault()
        $(e.target).parent().parent().next().find('.answer-container').css(
            {
                "visibility": "visible",
                "height": "auto",
                "width": "auto"
            }
        )
    })
    $('.mark-answer').on('click', function (e) {
        e.preventDefault()
        $(e.target).parent().addClass('bg-success');

        payload = { 'a_id': $(e.target).prev().val() }
        $.post("/answer/selected", payload, function (data) {
            window.location.href = window.location.href;
        });
    })
    $('.unmark-answer').on('click', function (e) {
        e.preventDefault()
        $(e.target).parent().removeClass('bg-success');

        payload = { 'a_id': $(e.target).prev().val() }
        $.post("/answer/unselected", payload, function (data) {

            window.location.href = window.location.href;
        });
    })
    $('.delete-answer').on('click', function (e) {
        e.preventDefault();
        if (confirm("Are you sure you want to delete this answer?")) {
            payload = { 'a_id': $(e.target).prev().prev().val() }
            $.post("/answer/delete", payload, function (data) {
                $(e.target).parent().remove()
            });
        }


    })




});