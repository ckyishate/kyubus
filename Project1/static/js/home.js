
msg = document.getElementById('error-msg')

if(msg != null){
    document.querySelector('.date-model').style.display = 'flex';
}
document.getElementById("dateBtn").addEventListener('click',
function(){
    document.querySelector('.date-model').style.display ='flex';
});

document.querySelector(".close").addEventListener('click',
 function(){
     document.querySelector('.date-model').style.display ='none';
     if(msg){
         msg.remove()
     }
    
});