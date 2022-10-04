
function populate(frm, data) {   
    $.each(data, function(key, value){  
    var $ctrl = $('[name='+key+']', frm);  
    switch($ctrl.attr("type"))  
    {  
        case "text" :   
        case "hidden":  
        $ctrl.val(value);   
        break;   
        case "radio" : case "checkbox":   
        $ctrl.each(function(){
           if($(this).attr('value') == value) {  $(this).attr("checked",value); } });   
        break;  
        default:
        $ctrl.val(value); 
    }  
    });  
}

$(function(){
    $(document).delegate('*[data-toggle="lightbox"]', 'click', function(event) {
        event.preventDefault();
        $(this).ekkoLightbox();
    });

    $('*[rel="tooltip"]').tooltip({html: true});

    $('.confirm_delete').click(function(){
        return confirm(CONFIRM_DELETE_MSG);
    });
    $.fm();
    
});
