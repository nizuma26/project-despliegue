let input_daterange;
let tblreportTras;

let report_tras = {
    list: function(all){
        let parameters = {
            'action': 'search_report',
            'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        };
        tblreportTras = $('#Report_Tras').DataTable({
            responsive: false,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: parameters,
                dataSrc: ""
            },
            order: false,
            paging: false,
            ordering: false,
            info: false,
            //searching: false,
            dom: 'Bfrtip',
            buttons: [
                {
                    extend: 'excelHtml5',
                    text: '<span class="badge badge-success" style="font-size:11px;"><i class="fas fa-file-excel"></i> EXCEL</span>',
                    titleAttr: 'Excel',
                    className: 'btn btn-success btn-xs',                    
                },
                {
                    extend: 'print',
                    text: '<span class="badge badge-info" style="font-size:11px;"><i class="fas fa-print"></i> IMPRIMIR</span>',
                    titleAttr: 'Imprimir Archivo',
                    footer: true,
                    className: 'btn btn-info btn-xs',                    
                },
                {
                    extend: 'pdfHtml5',
                    text: '<span class="badge badge-danger" style="font-size:11px;"><i class="fas fa-file-pdf"></i> PDF</span>',
                    titleAttr: 'PDF',
                    className: 'btn btn-danger btn-xs',
                    download: 'open',
                    orientation: 'landscape',
                    pageSize: 'LEGAL',
                    customize: function (doc) {
                        doc.styles = {
                            header: {
                                fontSize: 25,
                                bold: true,
                                alignment: 'center'
                            },
                            subheader: {
                                fontSize: 13,
                                bold: true
                            },
                            quote: {
                                italics: true
                            },
                            small: {
                                fontSize: 8
                            },
                            tableHeader: {
                                bold: true,
                                fontSize: 11,
                                color: 'white',
                                fillColor: '#2d4154',
                                alignment: 'center'
                            }
                        };
                        doc.content[1].table.widths = ['18%', '22%', '20%', '7%', '10%', '10%', '5%', '8%'];
                        doc.content[1].margin = [0, 35, 0, 0];
                        doc.content[1].layout = {};
                        
    
                    }
                }
            ],
            columns: [
                {"data": "position"},
                {"data": "prod"},
                {"data": "proddesc"},
                {"data": "tipo_tras"},
                {"data": "codbien"},
                {"data": "fecha"},
            ],
            language: {
                decimal: "",
                sLengthMenu: "Mostrar _MENU_ registros",
                emptyTable: "No hay información",
                info: "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
                infoEmpty: "Mostrando 0 a 0 de 0 Entradas",
                infoFiltered: "(Filtrado de _MAX_ total entradas)",
                infoPostFix: "",
                thousands: ",",
                lengthMenu: "Mostrar _MENU_ Entradas",
                loadingRecords: "Cargando...",
                processing: "Procesando...",
                searchPlaceholder: "Buscar",
                search: "<button type='button' class='btn btn-sm'><i class='fa fa-search'></i></button>",
                zeroRecords: "Sin resultados encontrados",
                paginate: {
                first: "Primero",
                last: "Ultimo",
                next: "<span class='fa fa-angle-double-right'></span>",
                previous: "<span class='fa fa-angle-double-left'></span>",
                },
                buttons: {
                copy: "Copiar", 
                print: "Imprimir",
                },
            },                
            initComplete: function (settings, json) {
    
            }
        });
    }
}
$(function () {
    input_daterange = $('input[name="date_range"]');

    input_daterange
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            }
        });

    $('.drp-buttons').hide();

    $('.btnSearch').on('click', function () {
        report_tras.list(false);
    });

});