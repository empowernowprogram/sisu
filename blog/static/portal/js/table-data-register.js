/*
    Script Added by Andy to deal with edit registration page
    Purpose: set up the data table with API from jquery and dynamically filter by registration type
*/
$(document).ready(function() {
    //Draw the data table with configurations below
    var table = $('#edit-employee-reg').DataTable({
        "language": {
            "info": "Showing _END_ of _TOTAL_ employees",
            "infoFiltered":   "(filtered)",
            "lengthMenu":     "Showing: _MENU_ entries",
            "paginate": {
                "next": "<i class='fa-solid fa-arrow-right' style='font-size:24px; transform:translate(0, 5px);'></i>", // or '→'
                "previous":  "<i class='fa-solid fa-arrow-left' style='font-size:24px; transform:translate(0, 5px);'></i>" // or '←' 
            }
        },
        "lengthMenu": [
            [10, 20, 50, -1],
            [10, 20, 50, 'All']
        ],
        "bFilter":true,
        "dom": "tip",         // This shows just the table
        initComplete: function () {
            let col_counter = 0;
            this.api().columns('.filter-col').every( function () {
                var column = this;
                col_counter += 1;

                var select = $(`<select class="table-sisu-select-option" id="search-id-${col_counter}"><option value="">All</option></select>`)
                    .appendTo($('#filter-select'))
                    
                    .on( 'change', function () {
                        var val = $.fn.dataTable.util.escapeRegex(
                            $(this).val()
                        );
 
                        column
                            .search( val ? '^'+val+'$' : '', true, false )
                            .draw();
                    } );
 
                column.data().unique().sort().each( function ( d, j ) {
                    console.log(d)
                    select.append( '<option value="'+d+'">'+d+'</option>' )
                } );
                
            } );

            
        }
        
    })

    
    //custom serach bar
    console.log(table)
    $('#search').keyup(function(){
        table.search($(this).val()).draw();
    })

    //custom filter bar
    table.page.len($('#showing').val()).draw();
    $('#showing').change(function(){
        console.log($(this).val());
        table.page.len($(this).val()).draw();
    })
   

})