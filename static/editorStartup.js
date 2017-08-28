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
    $("#clsEditor").click(function () {
        editor.setValue("");
    });
    $("#subEditor").click(function () {
        var title = $('#title').val();
        var content = editor.getValue();
        $.ajax({
            type: "POST",
            data: {
                _xsrf: $.cookie("_xsrf"),
                title: title,
                content: content
            },
            success: function() {
                if (typeof(title) != "undefined") {
                    window.location.reload();
                }
            }
        });
        editor.setValue("");
    });
});

