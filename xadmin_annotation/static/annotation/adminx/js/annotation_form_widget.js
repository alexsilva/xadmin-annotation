$(function () {
    $(".annotations-create").click(function () {
        var $el = $(this),
            csrftoken = $.getCookie('csrftoken'),
            for_id = $el.data("for_id"),
            $modal = $el.data("modal"),
            $container;
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
        $container = $modal.find(".modal-body");
        $.ajax({
            url: $el.data("add_url"),
            //data: {_fields: "user"},
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function (res, textStatus, jqXHR) {
                $container.html(res);
            }
        })
        $modal.modal();

    })
});