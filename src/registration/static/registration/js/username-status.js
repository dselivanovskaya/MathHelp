$("#id_username").change(function() {
    let username = $(this).val().trim();
    if (username != '') {
        $.ajax({
            url: '/username-status',
            type: 'get',
            data: {username: username},
            success: function(response) {
                if (response.result == 'success') {
                    document.getElementById('id_username').style.backgroundColor = '#DFF2BF';
                } else {
                    document.getElementById('id_username').style.backgroundColor = '#FFD2D2';
                }
            },
        });
    }
});
