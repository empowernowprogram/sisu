const track = document.querySelector('.carousel_track');
const slides = Array.from(track.children);
const nextButton = document.querySelector('.carousel_button--right');
const prevButton = document.querySelector('.carousel_button--left');
const navDots = document.querySelector('.carousel_nav');
const dots = Array.from(navDots.children);

const slideWidth = slides[0].getBoundingClientRect().width;

console.log(slideWidth);

// arrange slides next to each other

const setSlidePosition = (slide, index) => {
	slide.style.left = slideWidth * index + 'px';
};

slides.forEach(setSlidePosition);

const moveToSlide = (track, currentSlide, targetSlide) => {
	track.style.transform = 'translateX(-' + targetSlide.style.left + ')';
	currentSlide.classList.remove('current-slide');
	targetSlide.classList.add('current-slide');
}

// when i click left, move slides to left
prevButton.addEventListener('click', e => {
	const currentSlide = track.querySelector('.current-slide');
	const prevSlide = currentSlide.previousElementSibling;
	moveToSlide(track, currentSlide, prevSlide);	
})

// when i click right, move slides to right
nextButton.addEventListener('click', e => {
	const currentSlide = track.querySelector('.current-slide');
	const nextSlide = currentSlide.nextElementSibling;
	moveToSlide(track, currentSlide, nextSlide);
})

// when i click nav button, move to that slide
navDots.addEventListener('click', e => {
	//what indicator was clicked
	targetDot = e.target.closest('button');
	
	if (!targetDot) return;

	const currentSlide = track.querySelector('.current-slide');
	const currentDot = navDots.querySelector('.current-slide');
	const targetIndex = dots.findIndex(dot => dot === targetDot);
	const targetSlide = slides[targetIndex];
	

	moveToSlide(track, currentSlide, targetSlide);

	currentDot.classList.remove('current-slide');
	targetDot.classList.add('current-slide');
})