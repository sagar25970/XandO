$(function() {
        window.setInterval(function(){
            update()
        }, 1000)

        function update() {
            $.ajax({
            url: "/update",
            type: "POST",
            dataType: "json",
            success: function(data) {
                $(messages).replaceWith(data)
            }
        });
    }});