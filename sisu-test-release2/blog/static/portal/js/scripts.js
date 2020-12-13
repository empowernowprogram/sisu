$(document).ready(function() {
    // once dom is loaded and ready
    console.log('LOADED')
   
    let url  = window.location.href;
    let page = (url.split('/'));
    page_pathname = window.location.pathname;

    // // next get accordion side menu:
    let menu_hrefs = $('.page-sidebar-menu li a');
    for(let i=0; i<menu_hrefs.length; i++){
        let menu_href = $(menu_hrefs[i]).attr('href');

        if(menu_href === page_pathname){
            menu_class = $(menu_hrefs[i]).parent().parent().attr('class');

            if(menu_class === 'accordion-menu'){
                // no nested menu
                $(menu_hrefs[i]).parent().addClass('active-page');
            } else if (menu_class === 'sub-menu'){
                $(menu_hrefs[i]).parent().parent().parent().addClass('open');
                $(menu_hrefs[i]).parent().parent().parent().attr('style', 'display: block;');
                $(menu_hrefs[i]).parent().parent().attr('style', 'display: block;');
                
                let menu_sub_li = $(menu_hrefs[i]).parent().parent().find('li');

                for(let j=0; j<menu_sub_li.length; j++){
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
    $('.fa-edit').click(function() {
        $('#edit-reg-modal').modal('show');

        // assumption is table column count is static [name, email, registration]
        row_data = $(this).parent().parent().find('td');
        user_registration = row_data[2].innerText

        html_registration = `<select style="padding: 6px 6px; border: 1px solid #C1C7CD; border-radius: 4px">`

        if(user_registration.toLowerCase() === 'supervisor'){
            console.log(user_registration)
            html_registration += `<option value="supervisor" selected>Supervisor</option>`
            html_registration += '<option value="non-supervisor">Non-supervisor</option>'
        } else if (user_registration.toLowerCase() === 'non-supervisor'){
            html_registration += `<option value="supervisor">Supervisor</option>`
            html_registration += '<option value="non-supervisor" selected>Non-supervisor</option>'
        } else {
            html_registration += `<option value="supervisor">Supervisor</option>`
            html_registration += '<option value="non-supervisor">Non-supervisor</option>'
        }

        html_registration += '</select>'

        // updating modal data
        $('#user-name').empty();
        $('#user-email').empty();
        $('#user-registration').empty();

        $('#user-name').text(row_data[0].innerText);
        $('#user-email').text(row_data[1].innerText);
        $('#user-registration').html(html_registration);

    });


})