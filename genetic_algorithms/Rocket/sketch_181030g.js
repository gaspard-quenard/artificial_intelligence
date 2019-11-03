var population;
var lifespan = 350
//var lifeP;
var count = 0;
var target;

function setup() 
{
  createCanvas(400, 300);
  population = new Population();
  //lifeP = createP();
  
  target = createVector(width/2, 50);
}

function draw() 
{
  background(0);  
  population.run();
  count++;
  
  if (count == lifespan)
  {
      population.evaluate();
      population.selection();
      count = 0;
  }
  
  if (mouseIsPressed)
  {
    target.x = mouseX;
    target.y = mouseY;
  }
  
  fill(255);
  rect(rx1, ry1, rw1, rh1);
  rect(rx2, ry2, rw2, rh2);
  rect(rx3, ry3, rw3, rh3);
  
  ellipse(target.x, target.y, 16, 16);
}
