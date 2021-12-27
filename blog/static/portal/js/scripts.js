$(document).ready(function () {
    // once dom is loaded and ready
    console.log('LOADED')

    let url = window.location.href;
    let page = (url.split('/'));
    page_pathname = window.location.pathname;

    // // next get accordion side menu:
    let menu_hrefs = $('.page-sidebar-menu li a');
    for (let i = 0; i < menu_hrefs.length; i++) {
        let menu_href = $(menu_hrefs[i]).attr('href');

        if (menu_href === page_pathname) {
            menu_class = $(menu_hrefs[i]).parent().parent().attr('class');

            if (menu_class === 'accordion-menu') {
                // no nested menu
                $(menu_hrefs[i]).parent().addClass('active-page');
            } else if (menu_class === 'sub-menu') {
                $(menu_hrefs[i]).parent().parent().parent().addClass('open');
                $(menu_hrefs[i]).parent().parent().parent().attr('style', 'display: block;');
                $(menu_hrefs[i]).parent().parent().attr('style', 'display: block;');

                let menu_sub_li = $(menu_hrefs[i]).parent().parent().find('li');

                for (let j = 0; j < menu_sub_li.length; j++) {
                    $(menu_sub_li[j]).addClass('animation');
                }

                $(menu_hrefs[i]).parent().addClass('active-page');

            } else {
                console.log('error - could not find')
            }
            break;
        }
    }




    // edit registration
    $('.fa-edit').click(function () {
        $('#edit-reg-modal').modal('show');

        // assumption is table column count is static [name, email, registration]
        row_data = $(this).parent().parent().find('td');
        user_registration = row_data[2].innerText

        registration_option = ''

        if (user_registration.toLowerCase() === 'supervisor') {
            registration_option += `<option value="1" selected>Supervisor</option>`
            registration_option += '<option value="0" >Non-supervisor</option>'
        } else if (user_registration.toLowerCase() === 'non-supervisor') {
            registration_option += `<option value="1" >Supervisor</option>`
            registration_option += '<option value="0" selected>Non-supervisor</option>'
        } else {
            registration_option += `<option value="1" >Supervisor</option>`
            registration_option += '<option value="0" >Non-supervisor</option>'
        }

        // updating modal data
        $('#user-email').empty();
        $('#user-registration').empty();

        $('#user-email').text(row_data[1].innerText);
        $('#user-registration').html(registration_option);

        // update form input data
        $('#userName').val(row_data[0].innerText);
        $('#userEmail1').val(row_data[1].innerText);

    });

    $('.fa-trash').click(function () {
        $('#remove-user-modal').modal('show');

        // assumption is table column count is static [name, email, registration]
        row_data = $(this).parent().parent().find('td');
        user_registration = row_data[2].innerText

        // updating modal data
        $('#remove-user-name').empty();
        $('#remove-user-email').empty();

        $('#remove-user-name').text(row_data[0].innerText);
        $('#remove-user-email').text(row_data[1].innerText);

        // update form input data
        $('#userEmail2').val(row_data[1].innerText);

    });

    /* POST PROGRAM SURVEY SCRIPT - START */

    // when click on continue button
    $('.continueBtn').click(function (event) {
        // hide current question and show the next question
        if (event.target.id == "continue1") {
            $('#continue1').remove();
            $('#question2').show();
        } else if (event.target.id == "continue2") {
            $('#question1').hide();
            $('#question2').hide();
            $('#question3').show();
        }
    });

    // rating stars
    var $star_rating = $('.star-rating .fa');

    var SetRatingStar = function () {
        return $star_rating.each(function () {
            if (parseInt($star_rating.siblings('input.rating-value').val()) >= parseInt($(this).data('rating'))) {
                return $(this).removeClass('fa-star-o').addClass('fa-star');
            } else {
                return $(this).removeClass('fa-star').addClass('fa-star-o');
            }
        });
    };

    $star_rating.on('click', function () {
        $star_rating.siblings('input.rating-value').val($(this).data('rating'));
        $('#continue1').removeClass('disabled');
        return SetRatingStar();
    });

    // disable button for required field
    $("a").on("click", function (event) {
        if ($(this).hasClass("disabled")) {
            event.preventDefault();
        }
    });

    /* POST PROGRAM SURVEY SCRIPT - END */

    
    /* ADMIN REGISTRATION TEAM SCRIPT - START */

    var $team_expand = $('.triangle-right');

    $team_expand.on('mouseover', function () {
        $(this).attr('style', 'cursor: pointer;');
    });

    $team_expand.on('click', function () {
        team = $(this).attr('team');
        if ($(`#team-${team}`).is(":hidden")) {
            $('.team-table').hide();
            $(`#team-${team}`).show();
        } else {
            $(`#team-${team}`).hide();
        }
    });

    $('#add-team-btn').click(function () {
        $('#add-team-modal').modal('show');
    });

    $('.register-btn').click(function () {
        team_name = $(this).attr('team_name');
        team_id = $(this).attr('team_id');
        $('#team-id').text(team_id);
        $('#team').text(team_name);
        $('#registration-header').text(`Register Employees for ${team_name.toUpperCase()} Team`);

        $('#registration-step-1').hide();
        $('#registration-step-2').show();
    });

    $('.registration-back').click(function () {
        $('#registration-header').text('Register Employees');
        $('#registration-step-1').show();
        $('#registration-step-2').hide();
    });

    /* ADMIN REGISTRATION TEAM SCRIPT - END */
})