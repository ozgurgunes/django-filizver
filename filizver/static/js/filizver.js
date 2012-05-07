/*
    Initialising function for jQuery UI widgets
*/
$(document).ajaxComplete(function(){
    $('textarea.markup').each(function(){
        if (!$(this).data('wmd')) {
            $(this).data('wmd', true).wmd({
                helpLink: '/help/markdown',
                helpHoverTitle: 'Markdown help',
            });
        };
    });
});

$(document).ready(function(){
    /*
        Include django CSRF Token in every AJAX requests
    */
    $.ajaxSetup({ 
         beforeSend: function(xhr, settings) {
             function getCookie(name) {
                 var cookieValue = null;
                 if (document.cookie && document.cookie != '') {
                     var cookies = document.cookie.split(';');
                     for (var i = 0; i < cookies.length; i++) {
                         var cookie = jQuery.trim(cookies[i]);
                         // Does this cookie string begin with the name we want?
                         if (cookie.substring(0, name.length + 1) == (name + '=')) {
                             cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                             break;
                         }
                     }
                 }
                 return cookieValue;
             }
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         } 
    });
    
    $('textarea.markup').wmd({
        helpLink: '/help/markdown',
        helpHoverTitle: 'Markdown help',
    });

    /*
        Leaves commands
    */
    $('.posts').live('mouseenter', function(){
        $(this).children('.widget').show();
        if ($(this).children('figure').length > 0) {
            holder = $(this).children('figure');            
            $(this).children('menu.widget').position({
                of: holder,
                my: 'left top',
                at: 'left top',
                collision: 'none none',
            });
            $(this).children('form.widget').position({
                of: holder,
                my: 'right bottom',
                at: 'right bottom',
                offset: '-3 -3',
                collision: 'none none',
            });
        };
    }).live('mouseleave', function(){
        $(this).children('.widget').hide().animate();
    });
    
    
    $('.posts form.widget input').live('change', function(event){
        //this.form.submit();
        event.preventDefault();
        $.ajax({
              url: this.form.action,
              type: "POST",
              data: $(this.form).serialize(),
              success: function(data){
                $('#leaves').html(data);
              }
        });    
        
    })

    $('article#main nav li a').live('click', function(event) {
        event.preventDefault();
        $.get(this.href, function(data){
            $(data).appendTo('body').dialog({
                dialogClass: 'tabbed',
                buttons: {
                    Cancel: function(){
                        $(this).dialog.close();
                    }
                },
            }).tabs({selected: $(".tabbed ul li a.active").parent().index()});
        });
    });

    $('.post menu.commands a.delete').live('click', function(event){
        event.preventDefault();
        $.get(this.href, function(data){
            $(data).appendTo('body').dialog({
                width: 640,
            });
        });
    });    

    $('.post menu.commands a.update').live('click', function(event){
        event.preventDefault();
        $.get(this.href, function(data){
            $(data).appendTo('body').dialog({
                width: 640,
            });
        });
    });

    /*
        User relationships
    */        
    $('li#following a').click(function(event, xhr, settings){        
        event.preventDefault();
        $.ajax({
            url: this.href, 
            type: 'POST',
            success: function(feedback){$('li#following a').toggleClass('stop').toggleClass('start'); },
            error: function(feedback){alert(feedback.responseText);}
        }); 

    });
    
    /*
        Commenting
    */
    $('#comment_form form').live('submit', function(event){
        event.preventDefault();
        $.ajax({
              url: this.action,
              type: "POST",
              data: $(this).serialize(),
              success: function(data){
                $('#comment_form').html(data);
              }
        });    

    })
})
