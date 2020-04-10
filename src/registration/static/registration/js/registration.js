const PASSWD_MIN_LEN = 8;  // minimum password length
const RED = '#FFD2D2';    // shade of red
const GREEN = '#DFF2BF';  // shade of green

let PASSWDS_MATCH_MIN_LEN = false;


$('#id_username').change(function() {
/*
    Checks that username is not registered.
*/
    const username = $(this).val().trim();
    if (username != '') {
        $.ajax({
            url: '/api/users',
            type: 'get',
            data: {
                'username': username,
            },
            success: (response) => {
                if (response.length == 1) {
                    $(this).css({'background-color': RED});
                    $('#id_username_help').html(
                        'User with that username already exists.'
                    ).css({'color': 'red'});
                } else {
                    $(this).css({'background-color': GREEN});
                    $('#id_username_help').html('');
                }
            },
        });
    }
});


$('#id_email').change(function() {
/*
    Check that email is valid.
    Check that email is not registered.
*/
    const re = /\S+@\S+\.\S+/;
    const email = $(this).val().trim();

    if (email != '') {
        if (!re.test(email)) {
            $(this).css({'background-color': RED});
            $('#id_email_help').html(
                'Invalid email address.'
            ).css({'color': 'red'});
        } else {
            $.ajax({
                url: '/api/users',
                type: 'get',
                data: {
                    'email': email,
                },
                success: (response) => {
                    if (response.length == 1) {
                        $(this).css({'background-color': RED});
                        $('#id_email_help').html(
                            'User with that email already exists.'
                        ).css({'color': 'red'});
                    } else {
                        $(this).css({'background-color': GREEN});
                        $('#id_email_help').html('');
                    }
                },
            });
        }
    }
});


$('#id_password1, #id_password2').change(function() {
/*
    Check that password meets length requirements.
*/
    if ($(this).val().length < PASSWD_MIN_LEN) {
        PASSWDS_MATCH_MIN_LEN = false;
        $(this).css({'background-color': RED});
        $('#' + this.id + '_help').html(
            `Password must contain at least ${PASSWD_MIN_LEN} characters.`
        ).css({'color': 'red'});
    } else {
        PASSWDS_MATCH_MIN_LEN = true;
        $(this).css({'background-color': GREEN});
        $('#' + this.id + '_help').html('');
    }
});


$('#id_password2').change(function() {
/*
    Check that passwords match.
*/
    if (PASSWDS_MATCH_MIN_LEN) {
        if ($('#id_password1').val() != $('#id_password2').val()) {
            $(this).css({'background-color': RED});
            $('#id_password2_help').html("Passwords don't match.").css({'color': 'red'});
        } else {
            $(this).css({'background-color': GREEN});
            $('#id_password2_help').html('');
        }
    }
});
