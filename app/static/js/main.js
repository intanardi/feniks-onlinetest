$( document ).ready(function() {
    // START SCRIPT
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
    
    $(".delete-dialog",).on("click", function (e) {
    const getId = $(this).attr("target-id");
    const column_element = $(this).parent();
    const res = window.confirm("Are you sure you want to delete this data ?");
    if(!res){
        console.log(1);
        e.preventDefault();
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
        console.log(url)
        return false;
    }
            
    });
      // END OF SCRIPT
});

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

// document.addEventListener("keyup", function (e) {
//     var keyCode = e.keyCode ? e.keyCode : e.which;
//             if (keyCode == 44) {
//                 stopPrntScr();
//             }
//         });
function stopPrntScr() {

            var inpFld = document.createElement("input");
            inpFld.setAttribute("value", ".");
            inpFld.setAttribute("width", "0");
            inpFld.style.height = "0px";
            inpFld.style.width = "0px";
            inpFld.style.border = "0px";
            document.body.appendChild(inpFld);
            inpFld.select();
            document.execCommand("copy");
            inpFld.remove(inpFld);
        }
       function AccessClipboardData() {
            try {
                window.clipboardData.setData('text', "Access   Restricted");
            } catch (err) {
            }
        }
        // setInterval("AccessClipboardData()", 300);