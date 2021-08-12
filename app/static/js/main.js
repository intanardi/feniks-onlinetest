$( document ).ready(function() {

    var dropdown = document.getElementsByClassName("dropdown-btn");
    var i;

    for (i = 0; i < dropdown.length; i++) {
    dropdown[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var dropdownContent = this.nextElementSibling;
    if (dropdownContent.style.display === "block") {
    dropdownContent.style.display = "none";
    } else {
    dropdownContent.style.display = "block";
    }
    });
    }
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

    $(".delete-dialog-user",).on("click", function (e) {
        const getId = $(this).attr("target-id");
        const column_element = $(this).parent();
        const res = window.confirm("Are you sure you want to delete this user ?");
        if(!res){
            console.log(1);
            e.preventDefault();
        }else {
            $.ajax({
                type: "POST",
                url: "delete/"+ $(this).attr("target-id"),
                data: {
                    'name': 'delete-user',
                    'value': $(this).attr("target-id")
                },
                success: function () {
                    column_element.parent().hide(250)
                }
            });
            return false;
        }
            
    });

    $(".delete-dialog-candidate",).on("click", function (e) {
        const getId = $(this).attr("target-id");
        const column_element = $(this).parent();
        const res = window.confirm("Are you sure you want to delete this user ?");
        if(!res){
            console.log(1);
            e.preventDefault();
        }else {
            $.ajax({
                type: "POST",
                url: "delete/"+ $(this).attr("target-id"),
                data: {
                    'name': 'delete-candidate',
                    'value': $(this).attr("target-id")
                },
                success: function () {
                    column_element.parent().hide(250)
                }
            });
            return false;
        }
            
    });

    $(".delete-dialog-exam",).on("click", function (e) {
        // return alert(123)
        const getId = $(this).attr("target-id");
        const column_element = $(this).parent();
        const res = window.confirm("Are you sure you want to delete this user ?");
        if(!res){
            console.log(1);
            e.preventDefault();
        }else {
            $.ajax({
                type: "POST",
                url: "examination_delete/"+ $(this).attr("target-id"),
                data: {
                    'name': 'delete-examination',
                    'value': $(this).attr("target-id")
                },
                success: function () {
                    column_element.parent().hide(250)
                }
            });
            return false;
        }
            
    });
      // END OF SCRIPT
});