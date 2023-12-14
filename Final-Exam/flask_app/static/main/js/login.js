document.getElementById('sign-up').addEventListener('click', () =>{
    window.location.href = '/signup';
});

let count     = 0
function checkCredentials(event) {
    event.preventDefault()
    // package data in a JSON object
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var data_d = { 'email': email, 'password': password };

    // SEND DATA TO SERVER VIA jQuery.ajax({})
    jQuery.ajax({
        url: "/processlogin",
        data: data_d,
        type: "POST",
        success:function(returned_data){
              returned_data = JSON.parse(returned_data);
              if (returned_data.success) {
                  window.location.href = "/";
              } else {
                  count++;
                  document.getElementById('failed-attempts').textContent = 'Failed attempts: ' + count;
              }
        }
    });
}