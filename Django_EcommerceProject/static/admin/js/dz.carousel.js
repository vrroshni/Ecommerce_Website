/* JavaScript Document */


function carouselReview(){
	jQuery('.gallery-carousel').owlCarousel({
		margin:20,
		loop:true,
		autoWidth:true,
		items:4,
		autoplay:true,
		autoplayTimeout:1000,
		autoplayHoverPause:true,
		smartSpeed:1000,
		navText : ["<i class='fa fa-chevron-left'></i>","<i class='fa fa-chevron-right'></i>"]
	})
}


jQuery(window).on('load',function(){
	setTimeout(function(){
		carouselReview();
	}, 1000); 
});
/* Document .ready END */