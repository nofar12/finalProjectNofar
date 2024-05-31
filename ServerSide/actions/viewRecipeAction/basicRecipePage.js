
function open_close_nutritions_facts(){
        //change the arrow direction
        var degrees= document.getElementById("arrow-nutritions").style.transform
        if (!degrees || degrees == "rotateX(0deg)"){ // to open
            document.getElementById("arrow-nutritions").style.transform = "rotateX(180deg)"
            document.getElementById("nutritions-details").style.display = "inline"
            document.getElementById("nutrition-facts-basic").style.border = "none"
            document.getElementById("nutrition-facts").style.border = "1px solid black"
        }
        else{ //to close
            document.getElementById("arrow-nutritions").style.transform = "rotateX(0deg)"
            document.getElementById("nutritions-details").style.display = "none"
            document.getElementById("nutrition-facts-basic").style.border = "1px solid black"
            document.getElementById("nutrition-facts").style.border = "none"


        }

    }


function open_close_health_labels(){
        //change the arrow direction
        var degrees= document.getElementById("arrow-health").style.transform
        if (!degrees || degrees == "rotateX(0deg)"){ // to open
            document.getElementById("arrow-health").style.transform = "rotateX(180deg)"
            document.getElementById("health-details").style.display = "inline"
            document.getElementById("health-labels-basic").style.border = "none"
            document.getElementById("health-labels").style.border = "1px solid black"


        }
        else{ //to close
            document.getElementById("arrow-health").style.transform = "rotateX(0deg)"
            document.getElementById("health-details").style.display = "none"
            document.getElementById("health-labels-basic").style.border = "1px solid black"
            document.getElementById("health-labels").style.border = "none"

        }
}

function heart_clicked() {
        const recipeId = document.getElementById("recipe_id").value// get the recipe's id
        fetch("/view_recipe?action=like&id=" + recipeId ,{
           method: 'GET'
        })
        .then(response => response.json())
        .then( data => {
               document.getElementById("heart").src = data.imageLike
               document.getElementById("countLikes").innerHTML= data.likeCount
        })



}


function addReview() { //add comment\review
        const user_input =document.getElementById("reviewInput").value// get the user's input
        const recipe_id = document.getElementById("recipe_id").value// get the recipe's id
        review_data = {    //  json object of the data to send
            user_input: user_input,
            recipe_id: recipe_id
        }
        const reviewDataJson = JSON.stringify(review_data)
        // Send the data to the server using Fetch API
        fetch("/sumbit_review", {
            method: "POST",
            headers: { "Content-Type": "application/json"},
            body: reviewDataJson
           })
        .then(response => response.json())
        .then( data => {
               review_html ='<div class="review-card">' +
               '<img src="' + data.profile_pic + '" alt="Profile Picture" class="profilePicture">' +
                '<div class="review">'+
                '<h3>' + data.username +' says:</h3>'+
                ' <p>' + data.review  +'</p>'+
                '<p class= "time">' +data.time+'</p></div></div>'
               document.getElementById("reviews-cardsAll").innerHTML+= review_html
               document.getElementById("reviewInput").value= ""

        })


}


//document.addEventListener('DOMContentLoaded', function() {
//    var iframe = document.getElementById('embedded-iframe');
//    iframe.addEventListener('error', function() {
//        console.error('Error loading iframe');
//        iframe.style.display = 'none';
//    });
//});