document.getElementById('sign-in').addEventListener('click', () =>{
    window.location.href = '/login';
});

let count     = 0
function checkSignUp(event) {
    event.preventDefault()
    // package data in a JSON object
    var username = document.getElementById('username').value;
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var data_d = { 'username': username, 'email': email, 'password': password };

    // SEND DATA TO SERVER VIA jQuery.ajax({})
    jQuery.ajax({
        url: "/processsignup",
        data: data_d,
        type: "POST",
        success:function(returned_data){
              returned_data = JSON.parse(returned_data);
              if (returned_data.success) {
                  window.location.href = "/login";
              } else {
                  document.getElementById('failed-signup').textContent = returned_data.message;
              }
        }
    });
}