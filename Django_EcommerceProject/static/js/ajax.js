


function addToCart(id){
    console.log('hloo');



    $.ajax({
        url:'addtocart/' +id,
        method:get,
        success:(response)=>{

       swal("Good job!", "You clicked the button!", "success").then(()=>{

        
       })


        }
    })
}