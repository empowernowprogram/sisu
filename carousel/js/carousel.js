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

const updateDots = (currentDot, targetDot) => {
	currentDot.classList.remove('current-slide');
	targetDot.classList.add('current-slide');
}

const hideShowArrows = (slides, prevButton, nextButton, targetIndex) => {
	if (targetIndex === 0) {
		prevButton.classList.add('is-hidden');
		nextButton.classList.remove('is-hidden');
	} else if (targetIndex === slides.length - 1) {
		prevButton.classList.remove('is-hidden');
		nextButton.classList.add('is-hidden');
	} else {
		prevButton.classList.remove('is-hidden');
		nextButton.classList.remove('is-hidden');
	}
}

// when i click left, move slides to left
prevButton.addEventListener('click', e => {
	const currentSlide = track.querySelector('.current-slide');
	const currentDot = navDots.querySelector('.current-slide');
	const prevDot = currentDot.previousElementSibling;
	const prevSlide = currentSlide.previousElementSibling;
	const prevIndex = slides.findIndex(slide => slide == prevSlide);
	moveToSlide(track, currentSlide, prevSlide);	
	updateDots(currentDot, prevDot);
	hideShowArrows(slides, prevButton, nextButton, prevIndex);
})

// when i click right, move slides to right
nextButton.addEventListener('click', e => {
	const currentSlide = track.querySelector('.current-slide');
	const currentDot = navDots.querySelector('.current-slide');
	const nextDot = currentDot.nextElementSibling;
	const nextSlide = currentSlide.nextElementSibling;
	const nextIndex = slides.findIndex(slide => slide == nextSlide);
	moveToSlide(track, currentSlide, nextSlide);
	updateDots(currentDot, nextDot);
	hideShowArrows(slides, prevButton, nextButton, nextIndex);
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
	updateDots(currentDot, targetDot);
	hideShowArrows(slides, prevButton, nextButton, targetIndex);
	
})