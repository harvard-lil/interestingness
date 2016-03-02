var num_lines = 0;

function setup() {
	createCanvas(windowWidth, windowHeight);
	stroke('#FFFD00');
	fill('#FFFD00');
	//stroke('#f29');
	//fill('#f29');
	noLoop();
}

function draw() {
	var x,y;
	for (var i = 0; i < 50; i++) {
		x = floor(random(10, windowWidth -10));
		y = floor(random(10, windowHeight-10));
		beginShape();
		vertex(x, y);
		vertex(x + floor(random(10, 100)), y + floor(random(10, 100)));
		vertex(x + floor(random(10, 100)), y + floor(random(10, 100)));
		endShape(CLOSE);
	}
}