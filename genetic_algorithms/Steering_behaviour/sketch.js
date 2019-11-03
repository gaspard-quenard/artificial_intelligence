
var population = [];

var food = [];

var poison = [];

var hunters = []

var debug;

function setup()
{
  var canvas = createCanvas(800,600);


  for (var i = 0; i < 80; i++)
    food[i] = createVector(random(width),random(height));

  for (var i = 0; i < 30; i++)
    poison[i] = createVector(random(width),random(height));

  for (var i = 0; i < 10; i++)
    population[i] = new Vehicle(random(width), random(height));

  for (var i = 0; i < 3; i++)
    hunters[i] = new Hunter(random(width), random(height));

    debug = createCheckbox();
}

function mouseDragged()
{
  population.push(new Vehicle(mouseX, mouseY));
}

function draw()
{
  background(0);

  if (random(1) < 0.25)
    food.push(createVector(random(width),random(height)));
    if (random(1) < 0.01)
      poison.push(createVector(random(width),random(height)));

  fill(0, 255, 0);
  noStroke();
  for (var i = 0; i < food.length; i++)
    ellipse(food[i].x,food[i].y,4);

  fill(255, 0, 0);
  noStroke();
  for (var i = 0; i < poison.length; i++)
    ellipse(poison[i].x,poison[i].y,4);
/*
  var target = createVector(mouseX, mouseY);

  fill(127);
  stroke(200);
  strokeWeight(2);
  ellipse(target.x, target.y, 48);*/


  fill(127);

  for (var i = population.length -1; i >= 0; i--)
  {
    population[i].boundaries();
    population[i].behaviour(food, poison, hunters);
    population[i].update();
    population[i].display();

    var newVehicle = population[i].clone();
    if (newVehicle != null)
      population.push(newVehicle);

    if (population[i].dead())
    {
      food.push(createVector(population[i].position.x, population[i].position.y));
      population.splice(i,1);
    }

  }


  for (var i = 0; i < hunters.length; i++)
  {
    hunters[i].hunt(population);
    hunters[i].update();
    hunters[i].display();
  }

  //if (population.length > 10 * hunters.length)
  //  hunters.push(new Hunter(random(width), random(height)));
}
