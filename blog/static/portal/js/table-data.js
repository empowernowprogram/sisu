"use strict";

$(document).ready(function() {
    $('#edit-employee-reg').dataTable({
        "language": {
            "info": "Showing _START_ to _END_ of _TOTAL_ employees",
          },
        "lengthMenu": [[2, 10, 25, 50, -1], [2, 10, 25, 50, "All"]]
    })



    $('#employee-progress').DataTable( {
        "language": {
            "info": "Showing _START_ to _END_ of _TOTAL_ employees",
          },

        initComplete: function () {
            let col_counter = 0;
            this.api().columns([1, 2, 3, 3]).every( function () {
                var column = this;
                col_counter += 1;

                var select = $(`<select class="table-sisu-select-option" id="search-id-${col_counter}"><option value=""></option></select>`)
                    .appendTo( $(column.footer()).empty())
                    
                    .on( 'change', function () {
                        var val = $.fn.dataTable.util.escapeRegex(
                            $(this).val()
                        );
 
                        column
                            .search( val ? '^'+val+'$' : '', true, false )
                            .draw();
                    } );
 
                column.data().unique().sort().each( function ( d, j ) {
                    select.append( '<option value="'+d+'">'+d+'</option>' )
                } );
            } );
        }
    } );    
});