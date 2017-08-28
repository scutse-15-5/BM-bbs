$(document).ready(function () {
    $("#logout").click(function() {
        $.cookie("name", "", {expire: -1});
        $.cookie("psw", "", {expire: -1});
        window.location.reload();
    })
})