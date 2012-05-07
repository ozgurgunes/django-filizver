$(document).ajaxComplete(function () {
    var regexp = /\.(png)|(jpg)|(gif)$/i;
    var maxsize = 1024 * 1024 * 2;
    var uploadSequence = [];
    var uploadCounter = 0;
    var uploadNames = [];
    uploadSequence.start = function (index) {
        var next = this[index];
        if (next) {
            // Call the callback with any given additional arguments:
            next.apply(null, Array.prototype.slice.call(arguments, 1));
            this[index] = null;
        }
    };
    $('#photo_upload_form').each(function () {
        // Fix for browsers which support multiple file selection but not the File API:
        // https://github.com/blueimp/jQuery-File-Upload/issues#issue/36
        if (typeof File === 'undefined') {
            $(this).find('input:file').each(function () {
                $(this).removeAttr('multiple')
                    // Fix for Opera, which ignores just removing the multiple attribute:
                    .replaceWith($(this).clone(true));
            });
        }
    }).fileUploadUI({
        fieldName: 'image',
        namespace: 'file_upload',
        dropZone: $('#file_upload_container'),
        uploadTable: $('#file_upload_table'),
        downloadTable: $('#file_update_container'),
        cancelSelector: '.file_upload_cancel a',
        buildUploadRow: function (files, index) {
            return $('<tr><td class="file_upload_name">' + files[index].name + '<\/td>' +
                    '<td class="file_upload_progress"><div><\/div><\/td>' +
                    '<td class="file_upload_cancel"><a title="remove">remove</a></td></tr>');
        },
        buildDownloadRow: function (file) {
            return $('<div id="photo_'+file.id+'_update" class="row">'+file.update_form+'</div>');
        },
        beforeSend: function (event, files, index, xhr, handler, callBack) {
            uploadSequence.push(callBack);
            uploadNames.push(files[index].name);
            if (files[index].size > maxsize) {
                handler.uploadRow.find('.file_upload_progress').html(gettext('File is too big'));
                return;
            }
            if (!regexp.test(files[index].name)) {
                handler.uploadRow.find('.file_upload_progress').html(gettext('Only PNG, JPG & GIF image formats allowed'));
                return;
            }
            if (files[index].size === 0) {
                handler.uploadRow.find('.file_upload_progress').html(gettext('You have to choose a file'));
                return;
            }
            if (index > 4) {
                handler.uploadRow.find('.file_upload_progress').html(gettext('You can upload at most 5 images at once'));
                return;
            }
            handler.uploadRow.find('.file_upload_start button').click(function(event){
                event.preventDefault();
                callBack();
            });
            $('#start_uploads').click(function(event){
                event.preventDefault();
                uploadSequence.start(0);
            });
            $('#cancel_uploads').click(function(event){
                event.preventDefault();
                 $('.file_upload_cancel a').click();
            });

        },
        onComplete: function (event, files, index, xhr, handler) {
            initUI();
            uploadCounter++
            handler.onCompleteAll(files);
            uploadSequence.start(uploadCounter);
        },
        removeNode: function (node, callBack) {
            node.addClass('ui-state-highlight');
            node.children('.file_upload_cancel').remove();
            node.append('<td class="file_upload_complete"><span class="ui-icon ui-icon-check">Uploaded</span></td>');
            callBack();
        }, 
        onAbort: function (event, files, index, xhr, handler) {
            event.preventDefault();
            handler.uploadRow.remove();
            
            uploadSequence.splice(uploadNames.indexOf(files[index].name), 1)
            uploadNames.splice(uploadNames.indexOf(files[index].name), 1)
            
            handler.onCompleteAll(files, true);
        },
        onCompleteAll: function (files, abort) {            
            if(uploadCounter == uploadSequence.length && !abort) {
                /* your code after all uploads have completed */
                $('#photo_upload_form').slideUp(300, function(){
                    $(this).remove();
                });                
                $('#file_update_container').slideDown(300);                    
            }
        }
    });
});