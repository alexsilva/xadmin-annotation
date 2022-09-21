$(function () {
    $(".annotations-create").click(function () {
        var $el = $(this),
            for_id = $el.data("for_id"),
            $modal = $el.data("modal");
        if (!$modal) {
            $modal = $("#nunjucks-modal-main").template_render$({
                modal: {size: 'modal-lg'},
                cancel_button: {'class': 'btn-sm'},
                confirm_button: {
                    text: '<i class="confirm-icon"></i> Enviar',
                    class: for_id + "_send btn-sm"
                },
            }).appendTo('body');
            $el.data("modal", $modal)
        }

        $.ajax({

        })
        $modal.modal();

    })
});