let optGeneral = document.querySelector('#message');
let optPrice = document.querySelector('#request-price-quote');
let optDemo = document.querySelector('#request-demo');
let optDefault = document.querySelector('#default');
let content = document.querySelector('#content');

optGeneral.addEventListener('click', () => {
	content.innerHTML = `
	<div class="inner-content send-message">
		<label class = "important" for="subject">Subject</label>
			<input class = "long" type="text" name="subject">
		<label class = "important" for="message">Message</label>
<div>
<textarea id="message" rows="4" cols="50">
</textarea>
</div>
	</div>
	`
});

optDefault.addEventListener('click', () =>{
	content.innerHTML = ''
});

optDemo.addEventListener('click', () => {
	content.innerHTML = `
	<div class="inner-content demo">
		<div class="inner-inner">
			<label class="important" for="train-type">Trainings</label>
			<div class="checkline"><input type="checkbox" name="btnENP">Business Conduct Training: Empower Now Program</input></div>
			<div class="checkline"><input type="checkbox" name="btnMindglow">Active Shooter Training: Mindglow</input></div>
		</div>
		<div class="message">	
		<label class="optional" for="message">Message (optional)</label>
<div>
<textarea id="message" rows="4" cols="50">
</textarea>
</div>
</div>
	</div>
	`
});

optPrice.addEventListener('click', () => {
	content.innerHTML = `
	<div class="inner-content price-quote">
				<label class="important" for="address">Company Address</label>
					<input class = "all long" type="text" name="address">
				<label class="important" for="num-employees">Number of Employees</label>
					<input class = "short" type="number" name="num-employees">
				<div>
					<label class="important" for="train-type">Trainings</label>
					<div class="checkline"><input type="checkbox" name="btnENP">Business Conduct Training: Empower Now Program</input></div>
					<div class="checkline"><input type="checkbox" name="btnMindglow">Active Shooter Training: Mindglow</input></div>
				</div>	
				<div class="message">
				<label class="optional" for="message">Message (optional)</label>
<div>
<textarea id="message" rows="4" cols="50">
</textarea>
</div>
</div>
			</div>
	`	
});