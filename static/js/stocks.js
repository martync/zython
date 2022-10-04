// var modal_id_element = "id_main_modal";


$(function(){
    $.fm({debug: true});

    // $(".modal_open").click(function(){
    //     title = $(this).data("modal-title");
    //     url = $(this).data("modal-url");
    //     $.get(url, function(response){
    //         $("#"+modal_id_element+" h4").text(title);
    //         $("#"+modal_id_element).modal("show");
    //         show_ajax_form(response);

    //     });
    // });

    // $("#modal_form_submit").click(function(){
    //     send_ajax_form()
    // });
});



// function send_ajax_form(){
//     form = $("#"+modal_id_element).find("form:first");
//     url = form.attr("action");
//     $.ajax({
//         type: "POST",
//         url: url,
//         data: form.serialize(),
//         success: function(data, textStatus, xhr){
//             new_location = xhr.getResponseHeader('Location');
//             if (new_location){
//                 document.location.href = new_location;
//             }
//             if (xhr.status == 202){
//                 reload_page();
//             }
//             if (xhr.status == 200){
//                 show_ajax_form(data);
//             }
//         }
//     });
// }

// function reload_page(){
//     document.location.href = ".";
// }

// function show_ajax_form(data){
//     $("#"+modal_id_element+" #xhr_content").html(data);
//     init_widgets();
// }

