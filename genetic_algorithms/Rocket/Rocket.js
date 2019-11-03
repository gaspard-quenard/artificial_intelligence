var rx1 = 140;
var ry1 = 140;
var rw1 = 130;
var rh1 = 10;

var rx2 = 100;
var ry2 = 0;
var rw2 = 20;
var rh2 = 140;

var rx3 = 250;
var ry3 = 0;
var rw3 = 20;
var rh3 = 140;



function Rocket(dna)
{
  this.pos = createVector(width/2, height);
  this.vel = createVector();
  this.acc = createVector();
  this.crashed = false;

  if (dna)
    this.dna = dna;
  else
    this.dna = new DNA();
  this.fitness = 0;

  this.applyForce = function(force)
  {
    this.acc.add(force);
  }

  this.update = function()
  {

    if (this.pos.x > rx1 && this.pos.x < rx1 + rw1
      && this.pos.y > ry1 && this.pos.y < ry1 + rh1)
    {
      this.crashed = true;
    }

    if (this.pos.x > rx2 && this.pos.x < rx2 + rw2
      && this.pos.y > ry2 && this.pos.y < ry2 + rh2)
    {
      this.crashed = true;
    }
    
    if (this.pos.x > rx3 && this.pos.x < rx3 + rw3
      && this.pos.y > ry3 && this.pos.y < ry3 + rh3)
    {
      this.crashed = true;
    }

    this.applyForce(this.dna.genes[count]);

    if (!this.crashed)
    {
      this.vel.add(this.acc);
      this.pos.add(this.vel);
      this.acc.mult(0);
    }
  }

  this.show = function()
  {
    push();
    noStroke();
    fill(255, 150);
    translate(this.pos.x, this.pos.y);
    rotate(this.vel.heading());
    rectMode(CENTER);
    rect(0, 0, 25, 5);
    pop();
  }

  this.calcFitness = function()
  {
    var d = dist(this.pos.x, this.pos.y, target.x, target.y); 
    this.fitness = 1 / pow(d,3);

    if (this.crashed)
      this.fitness /= 100;
    //this.fitness = map(d, 0, width, width, 0);
  }

  this.collision = function(x, y, w, h)
  {
    if (this.pos.x > x && this.pos.x < x + w
      && this.pos.y > y && this.pos.y < y + h)
    {
      return true;
    }
    return false;
  }
}
