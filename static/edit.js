$(document).ready(function () {
    var editor = new Simditor({
        textarea: $('#editor'),
        toolbar: [
            'title',
            'bold',
            'italic',
            'underline',
            'strikethrough',
            'fontScale',
            'color',
            'ol',
            'ul',
            'blockquote',
            'code',
            'table',
            'link',
            'image',
            'hr',
            'indent',
            'outdent',
            'alignment',
            'html'
        ],
        pasteImageL: true,
        imageButton: [
            'upload',
            'external'
        ]
    });

    var topic_id;
    function getTopicId(node) {
        var href = node.attr("href");
        return href.substr(11);
    }
    $(".edit").click(function () {
        topic_id = getTopicId($(this).siblings(".btn-info"));
        $.ajax({
            type: "POST",
            data: {
                _xsrf: $.cookie("_xsrf"),
                status: 1,
                id: topic_id
            },
            success: function (data) {
                var content = data;
                editor.setValue(content);
            }
        });
    });

    $(".delete").click(function () {
        topic_id = getTopicId($(this).siblings(".btn-info"));
        $.ajax({
            type: "POST",
            data: {
                _xsrf: $.cookie("_xsrf"),
                status: 0,
                id: topic_id
            },
            success: function () {
                window.location.reload();
            }
        });
    });

    $("#subEditor").click(function () {
        var content = editor.getValue();
        $.ajax({
            type: "POST",
            data: {
                status: 2,
                id: topic_id,
                content: content
            },
        });
    });

    $("#uploadIcon").click(function() {
        var icon = $("#icon").val();
        $.ajax({
            url: "/icon",
            type: "POST",
            data: {
                _xsrf: $.cookie("_xsrf"),
                icon: icon
            }
        })
    });
});