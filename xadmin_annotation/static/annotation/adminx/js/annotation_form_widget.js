$(function () {
    $(".annotations").click(function () {
        var $el = $(this),
            csrftoken = $.getCookie('csrftoken'),
            for_id = $el.data("for_id"),
            object_id = $el.data('object_id'),
            object_key = $el.data('object_key'),
            filter_prefix = $el.data('filter_prefix'),
            page_param = $el.data('page_param'),
            $modal = $el.data("modal"),
            $container;
        if (!$modal) {
            $modal = $("#nunjucks-modal-main").template_render$({
                header: {title: $el.data('title')},
                modal: {size: 'modal-lg'},
                cancel_button: {
                    'class': 'btn-sm',
                    text: '<i class="fa fa-times" aria-hidden="true"></i> ' + gettext("Close")
                },
            }).appendTo('body');
            $el.data("modal", $modal)
        }
        $container = $modal.find(".modal-body");
        var fields = ["user", "description", "tb_created"],
            mask_tmpl = '<div class="mask {{classes}}"><{{header|default("h3")}} style="text-align:center;"><i class="{{icon}}"></i>{{text|safe}}</{{header|default("h3")}}></div>',
            $mask = $($.fn.nunjucks_env.renderString(mask_tmpl, {icon: 'fa-spinner fa-spin fa fa-large'})),
            $reload = $($.fn.nunjucks_env.renderString(mask_tmpl, {
                icon: 'fa fa-exclamation-circle text-danger',
                classes: 'annotation-retry',
                text: $.fn.nunjucks_env.renderString(
                    '<a href="javascript:(window.xadmin.load_annotation_list($(\'div.annotation-retry\').data(\'page_num\')));">{{msg}}</a>',
                    {msg: gettext("Failed to load data.")},
                ),
                header: "h6"
            })),
            render_item = function ($table, res) {
                var index,
                    index_inner,
                    field, value,
                    results = res.objects,
                    $thead = $("<thead>").appendTo($table),
                    $tbody = $("<tbody>").appendTo($table),
                    $headers = $("<tr>").appendTo($thead),
                    $rows, $cols,
                    $btn;

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
                        $cols = $('<td>').appendTo($rows);
                        $cols.html($('<div/>').html(value).text());
                    }
                }
                var go_page = function (options) {
                    if (!options.classes)
                        options.classes = "btn btn-secondary";
                    var content = "{% if icon %}<i class='{{icon}}' aria-hidden='true'></i>{% endif %} {{text}}";
                    $btn = $("<button>", {
                        type: "button",
                        class: options.classes,
                    }).html($.fn.nunjucks_env.renderString(content, {
                        icon: options.icon,
                        text: options.text
                    }));
                    if (!options.event) {
                        options.event = function () {
                            $btn.find("i").addClass("fa fa-sm fa-spinner fa-spin");
                            load_annotation_list(options.page_num);
                        }
                    }
                    $btn.click(options.event)
                    $container.append($btn);
                    return $btn
                }
                if (res.has_more || res.page_num > 0) {
                    go_page({
                        page_num: res.page_num - 1,
                        icon: "fa fa-backward",
                        text: gettext('Back'),
                        classes: "btn btn-primary"
                    }).prop('disabled', res.page_num <= 0);
                }
                if (res.has_more) {
                    go_page({
                        page_num: res.page_num + 1,
                        text: gettext('Next'),
                        classes: "btn btn-primary",
                        icon: "fa fa-forward",
                        event: function () {
                            var $loading = $btn.find("i")
                                .addClass("fa fa-sm fa-spinner fa-spin")
                                .removeClass("d-none");
                            load_annotation_list(res.page_num + 1).always(function () {
                                $loading.addClass("d-none");
                            })
                        }
                    });
                } else if (res.page_num > 0) {
                    go_page({
                        page_num: 0,
                        icon: "fa fa-home",
                        text: gettext('Start')
                    });
                }
            },
            load_annotation_list = function (page_num) {
                var params = {_fields: fields.join(",")}
                params[page_param] = page_num;
                // filter
                if (!object_id) {
                    // instance creation
                    params[filter_prefix + "key__in"] = object_key;
                } else {
                    // instance update
                    params[filter_prefix + "object_id__exact"] = object_id;
                }
                return $.ajax({
                    url: $el.data("url"),
                    data: params,
                    beforeSend: function (xhr, settings) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        $container.html($mask);
                        $mask.show();
                    },
                    success: function (res, textStatus, jqXHR) {
                        var $tb = $("<table class='table table-striped table-bordered table-sm'></table>");
                        $container.html($tb);
                        render_item($tb, res);
                    }
                }).always(function () {
                    setTimeout(function () {
                        $mask.hide();
                    }, 500);

                }).fail(function () {
                    setTimeout(function () {
                        $reload.data('page_num', page_num);
                        $container.html($reload);
                        $reload.show();
                    }, 500);
                });
            }
        window.xadmin.load_annotation_list = load_annotation_list;
        load_annotation_list(0);
        $modal.modal();
    })
});