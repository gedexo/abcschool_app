$(function () {
    'use strict'

    $(document).on("change", "#image_update_form input[type=file]", function () {
        var $this = $(this);
        var file = this.files[0];
        var reader = new FileReader();
        reader.onloadend = function () {
            $this
                .closest(".avatar-xxl")
                .css("background-image", "url(" + reader.result + ")");
        };
        if (file) {
            reader.readAsDataURL(file);
            $.ajax({
                type: "POST",
                url: "/accounts/profile/",
                data: new FormData($("#image_update_form")[0]),
                processData: false,
                contentType: false,
                success: function (data) {
                    console.log(data);
                    location.reload();
                },
                error: function (data) {
                    console.log(data);
                }
            });

        }
    });


});
