const input = document.querySelector("#phone");
const error_msg=document.getElementById("error_msg");

    const ho= window.intlTelInput(input, {
         initialCountry:'NP',
         loadUtils: () => import("https://cdn.jsdelivr.net/npm/intl-tel-input@26.9.1/build/js/utils.js"),
      });

document.getElementById("contactForm").addEventListener('submit',function(e){
    if(ho.isValidNumber()){
        input.value=ho.getNumber()
        error_msg.style.display='none';
    }
    else{
        error_msg.style.display='inline';
        e.preventDefault()
    }
})
   