$(function () {
    $('#entry_form').fileupload({
        dataType: 'json',
        uploadTemplateId: null,
        downloadTemplateId: null,
        uploadTemplate: function (o) {
                var rows = $();
                $.each(o.files, function (index, file) {
                    var row = $('<tr class="template-upload fade">' +
                        '<td class="preview"><span class="fade"></span></td>' +
                        '<td class="name"></td>' +
                        '<td class="size"></td>' +
                        (file.error ? '<td class="error" colspan="2"></td>' :
                                '<td><div class="progress">' +
                                    '<div class="bar" style="width:0%;"></div></div></td>' +
                                    '<td class="start"><button class="btn">Start</button></td>'
                        ) + '<td class="cancel"><button class="btn">Cancel</button></td></tr>');
                    row.find('.name').text(file.name);
                    row.find('.size').text(o.formatFileSize(file.size));
                    if (file.error) {
                        row.find('.error').text(file.error);
                    }
                    rows = rows.add(row);
                });
                return rows;
            },
            downloadTemplate: function (o) {
                var rows = $();
                $.each(o.files, function (index, file) {
                    var row = $('<tr class="template-download fade">' +
                        (file.error ? '<td></td><td class="name"></td>' +
                            '<td class="size"></td><td class="error" colspan="2"></td>' :
                                '<td class="preview"></td>' +
                                    '<td class="name"><a></a></td>' +
                                    '<td class="size"></td><td colspan="2"></td>'
                        ) + '<td class="delete"><button class="btn">Delete</button> ' +
                            '<input type="checkbox" name="delete" value="1"></td></tr>');
                    row.find('.size').text(o.formatFileSize(file.size));
                    if (file.error) {
                        row.find('.name').text(file.name);
                        row.find('.error').text(file.error);
                    } else {
                        row.find('.name a').text(file.name);
                        if (file.thumbnail_url) {
                            row.find('.preview').append('<a><img></a>')
                                .find('img').prop('src', file.thumbnail_url);
                            row.find('a').prop('rel', 'gallery');
                        }
                        row.find('a').prop('href', file.url);
                        row.find('.delete button')
                            .attr('data-type', file.delete_type)
                            .attr('data-url', file.delete_url);
                    }
                    rows = rows.add(row);
                });
                return rows;
            }
    });
});