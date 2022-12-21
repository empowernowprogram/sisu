/* 

1. Add your custom JavaScript code below
2. Place the this code in your template:

  

*/

var slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides((slideIndex += n));
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides((slideIndex = n));
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");
  if (n > slides.length) {
    slideIndex = 1;
  }
  if (n < 1) {
    slideIndex = slides.length;
  }
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex - 1].style.display = "block";
  dots[slideIndex - 1].className += " active";
}

function galleryFunction(img) {
  var video = document.getElementById("video-container");
  video.style.display = "none";
  var expandImg = document.getElementById("expandedImg");
  expandImg.src = img.src;
  expandImg.style.display = "block";
}

function galleryVideo(vid) {
  var expandImg = document.getElementById("expandedImg");
  expandImg.style.display = "none";

  var video = document.getElementById("video-container");
  video.style.display = "block";
}
