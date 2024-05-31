function homepage(){
    location.href = '/homepageUser/homepageUser.html';
}


function acc_settings(){
    location.href = '/accountSettings/accountSettings.html';
}


function favorites(){
    location.href = '/myFavorites/myFavorites.html';

}

function open_close_menu(){
    //change the arrow direction
    var arrow = document.getElementById("arrow-profile")
    var degrees= arrow.style.transform
    if (!degrees || degrees == "rotateX(0deg)"){ // to open
       arrow.style.transform = "rotateX(180deg)"
       document.getElementById("shortcuts-menu").style.display = "inline"
    }
    else{ //to close
         arrow.style.transform = "rotateX(0deg)"
         document.getElementById("shortcuts-menu").style.display = "none"

    }
}