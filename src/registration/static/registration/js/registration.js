
const RED = '#FFD2D2';    // shade of red
const GREEN = '#DFF2BF';  // shade of green

$('#id_username').change(function() {
    const username = $(this).val().trim();
    if (username != '') {
        $.ajax({
            url: '/api/users',
            type: 'get',
            data: {
                'username': username,
            },
            success: (response) => {
                if (response.length == 1)
                    $(this).css({'background-color': RED});
                else
                    $(this).css({'background-color': GREEN});
            },
        });
    }
});

$('#id_email').change(function() {
    const email = $(this).val().trim();
    if (email != '') {
        $.ajax({
            url: '/api/users',
            type: 'get',
            data: {
                'email': email,
            },
            success: (response) => {
                if (response.length == 1)
                    $(this).css({'background-color': RED});
                else
                    $(this).css({'background-color': GREEN});
            },
        });
    }
});
