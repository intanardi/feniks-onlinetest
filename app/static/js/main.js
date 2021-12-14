$( document ).ready(function() {
    // START SCRIPT

    document.addEventListener("contextmenu", function (e) {
        e.preventDefault();
    }, false);

    $( "#repasswordF, #passwordF" ).keyup(function(e) {
        var password = $("#passwordF").val();
        var confirm_password = $("#repasswordF").val();
            if(password != confirm_password) {
              $("#password-message").removeClass("text-success");
              $("#password-message").addClass("text-danger");
               $("#password-message").text('Password Different !');
            }
            else{
               $("#password-message").removeClass("text-danger");
               $("#password-message").addClass("text-success");
               $("#password-message").text('Password Validated !');
            }
      });
    
    $(".confirmation-candidate").on("click", function (e) {
        const res = window.confirm("Update confirmation ?");
        e.preventDefault();
        if(!res){
            console.log(1);
        }else {
            $.ajax({
                type: "POST",
                url: "update_status_psikotest/"+ $(this).attr("target_candidate_id"),
                data: {
                    'name': 'delete-dialog',
                    'value': $(this).attr("target-id")
                },
                success: function (response) {
                    console.log(response)
                    window.location.href = response;
                }
            });
        }
                
    });
    
    $(".delete-dialog",).on("click", function (e) {
    const getId = $(this).attr("target-id");
    const column_element = $(this).parent();
    const res = window.confirm("Are you sure you want to delete this data ?");
    e.preventDefault();
    if(!res){
        console.log(1);
    }else {
        $.ajax({
            type: "POST",
            url: "delete/"+ $(this).attr("target-id"),
            data: {
                'name': 'delete-dialog',
                'value': $(this).attr("target-id")
            },
            success: function () {
                column_element.parent().hide(250)
                console.log(123)
            }
        });
        return false;
    }
            
    });
      // END OF SCRIPT
});

$(".edit-evaluation").on("click", function(e){
    const getId = $(this).attr("target-id");
    // const getlink = $(this).attr("target-link");
    const getAction = $(this).attr("action-type");
    const urlhref = $(this).attr("myurl");
    console.log($(this).attr("href"));
    console.log(123)
    const column_element = $(this).parent();
    console.log(getId)
    var tdelement = $(this).parent();
    console.log(tdelement)
    if (getAction == 3) {
        tdelement.append('<span><a class="btn btn-sm btn-danger text-white" href="'+urlhref+'" title="Nyatakan Gagal" getAction="'+getAction+'" getId="'+getId+'">Gagal</a> <button class="btn btn-sm btn-outline-danger closeEvaluation" title="Close"><i class="fa fa-times"></i></button></span>');
    } else if(getAction == 2) {
        tdelement.append('<span><a class="btn btn-sm btn-success text-white" href="'+urlhref+'" title="Nyatakan Lolos" getAction="'+getAction+'" getId="'+getId+'">Lolos</a> <button class="btn btn-sm btn-outline-danger closeEvaluation" title="Close"><i class="fa fa-times"></i></button></span>');
    }
    $(this).css("display", "none");
});

// function closeEvaluation(e){
//     const editElement = e.parentElement.parentElement ;
//     e.parentElement.remove();
// }
$('.tbelement').on('click', '.setGranted', function(e) {
    e.preventDefault();
    const getAction = $(this).attr("getAction");
    const getId = $(this).attr("getId");
    let res = null;
    if (getAction == 2) {
     res = window.confirm("Anda yakin kandidat ini lolos ?");
    } else {
     res = window.confirm("Anda yakin kandidat ini gagal ?");
    }
    if(!res){
        console.log(1);
    }else {
    $.ajax({
        type: "POST",
        url: "/test/result/set_granted/"+ getId,
        data: {
            'id': getId,
            'value': getAction
        },
        success: function () {
            location.reload();
        }
    });
    return false;
     }
 });


 $('.tbelement').on('click', '.closeEvaluation', function(e) {
    const parent1 = $(this).parent();
    const parent2 = parent1.parent();
    const editEl = parent2.find('.edit-evaluation');
    editEl.css("display", "inline-flex");
    parent1.remove()
 });
// $( ".edit-evaluation" ).toggle(
//     function() {
//         const getId = $(this).attr("target-id");
//         const getlink = $(this).attr("target-link");
//         const column_element = $(this).parent();
//         console.log(getId)
//         var tdelement = $(this).parent();
//         $(this).remove();
//     }, function() {
//       $( this ).removeClass( "selected" );
//     }
//   );

$(".duration-check",).on("keydown", function (e) {
    console.log("duration")
    // Only ASCII character in that range allowed
    var ASCIICode = (e.which) ? e.which : e.keyCode
    if (ASCIICode > 31 && (ASCIICode < 48 || ASCIICode > 57)) {
        $("#error-message").addClass("text-danger");
        $("#error-message").text('Set Duration in number Only');
    }
    else {
        $("#error-message").removeClass("text-danger");
        $("#error-message").text('');
    }
});

$(".backButton").click(function(){
    window.history.go(-1);
});

const lalert = $('#alertshow');
if (lalert.is(":checked")) {
    $("#alertBox").show() ;
}

$('#alertShow').click(function() {
    // $("#alertBox").toggle(this.checked);
    if(this.checked) {
        $("#alertBox").show() ;
    } else {
        $("#alertBox").hide() ;
        $("#alertBox").val(""); 
    }
});