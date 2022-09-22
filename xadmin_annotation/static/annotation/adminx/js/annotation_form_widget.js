$(function () {
    $(".annotations").click(function () {
        var $el = $(this),
            csrftoken = $.getCookie('csrftoken'),
            for_id = $el.data("for_id"),
            object_id = $el.data('object_id'),
            filter_prefix = $el.data('filter_prefix'),
            $modal = $el.data("modal"),
            $container;
        if (!$modal) {
            $modal = $("#nunjucks-modal-main").template_render$({
                modal: {size: 'modal-lg'},
                cancel_button: {'class': 'btn-sm'}
            }).appendTo('body');
            $el.data("modal", $modal)
        }
        $container = $modal.find(".modal-body");
        var fields = ["user", "description"],
            render_item = function ($table, res) {
                var index,
                    index_inner,
                    field, value,
                    results = res.objects,
                    $thead = $("<thead>").appendTo($table),
                    $tbody = $("<tbody>").appendTo($table),
                    $headers = $("<tr>").appendTo($thead),
                    $rows;

                Object.keys(res.headers).forEach(function (key) {
                    $headers.append($.fn.nunjucks_env.renderString("<td>{{text}}</td>", {
                        text: res.headers[key]
                    }));
                })
                for (index = 0; index < results.length; index++) {
                    $rows = $("<tr>").appendTo($tbody);
                    for (index_inner = 0; index_inner < fields.length; index_inner++) {
                        field = fields[index_inner];
                        value = results[index][field];
                        $rows.append($.fn.nunjucks_env.renderString("<td>{{text}}</td>", {
                            text: value
                        }));
                    }
                }
                if (!res.has_more) {
                    var $btn = $("<button>",{
                        type: "button",
                        class: "btn btn-secondary"
                    }).html("<i class='d-none'></i>Carregar mais...");
                    $btn.click(function (){
                        var $loading = $btn.find("i")
                            .addClass("fa fa-sm fa-spinner fa-spin")
                            .removeClass("d-none");
                        load_data(res.page_num + 1).always(function (){
                            $loading.addClass("d-none");
                        })
                    })
                    $container.append($btn)
                }
            },
            load_data = function (page_num) {
                var params = {
                    page: page_num,
                    _fields: fields.join(",")
                }
                // filter
                params[filter_prefix + "object_id__exact"] = object_id;
                return $.ajax({
                    url: $el.data("url"),
                    data: params,
                    beforeSend: function (xhr, settings) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    },
                    success: function (res, textStatus, jqXHR) {
                        var $tb = $("<table class='table'></table>");
                        $container.html($tb);
                        render_item($tb, res);
                    }
                })
            }
        load_data(1);
        $modal.modal();
    })
});