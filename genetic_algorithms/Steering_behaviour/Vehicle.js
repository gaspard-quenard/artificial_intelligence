var mutationRate = 0.01

var Vehicle = function(x, y, dna)
{
  this.acceleration = createVector(0,0);
  this.velocity = createVector(0, -2);
  this.position = createVector(x,y);
  this.r = 4;
  this.maxSpeed = 5;
  this.maxForce = 0.5;

  this.health = 1.5;

  this.dna = [];

  if (dna === undefined)
  {
    //food weight
    this.dna[0] = random(-2, 2);
    //poison weight
    this.dna[1] = random(-2, 2);
    //food perception
    this.dna[2] = random(0, 100);
    //poison perception
    this.dna[3] = random(0, 100);
    //hunter weight
    this.dna[4] = random(-2, 2);
    //hunter perception
    this.dna[5] = random(30, 150);

}
else
{
  this.dna[0] = dna[0];
  if (random(1) < mutationRate)
    this.dna[0] += random(-0.1, 0.1);
  this.dna[1] = dna[1];
  if (random(1) < mutationRate)
    this.dna[0] += random(-0.1, 0.1);
  this.dna[2] = dna[2];
  if (random(1) < mutationRate)
    this.dna[0] += random(-10, 10);
  this.dna[3] = dna[3];
  if (random(1) < mutationRate)
    this.dna[0] += random(-10, 10);

  this.dna[4] = dna[4];
  if (random(1) < mutationRate)
    this.dna[4] += random(-0.1, 0.1);
  this.dna[5] = dna[5];
  if (random(1) < mutationRate)
    this.dna[5] += random(-10, 10);
}

  this.update = function()
  {
    this.health -= 0.005;
    this.velocity.add(this.acceleration);
    this.velocity.limit(this.maxSpeed);
    this.position.add(this.velocity);

    this.acceleration.mult(0);
  }

  this.applyForce = function(force)
  {
    this.acceleration.add(force);
  }

  this.behaviour = function(good, bad, hunters)
  {
    var foodSteer = this.eat(good, 0.1, this.dna[2]);
    var poisonSteer = this.eat(bad, -0.5, this.dna[3]);
    var hunterSteer = this.flee(hunters, this.dna[5]);

    foodSteer.mult(this.dna[0]);
    poisonSteer.mult(this.dna[1]);
    hunterSteer.mult(this.dna[4]);

    this.applyForce(hunterSteer);
    this.applyForce(foodSteer);
    this.applyForce(poisonSteer);

  }

  this.clone = function()
  {
    if (random(1) < 0.003)
      return new Vehicle(this.position.x, this.position.y, this.dna);
    else
      return null;
  }


  this.flee = function(hunters, perception)
  {
    for (var i = hunters.length -1; i >= 0; i--)
    {
      var d = dist(hunters[i].position.x, hunters[i].position.y, this.position.x, this.position.y);
      if (d < perception)
      {
        return this.seek(hunters[i].position)
      }
    }
    return createVector(0,0);
  }

  this.eat = function(food, nutrition, perception)
  {
    var record = Infinity;
    var closest = null;
    for (var i = food.length -1; i >= 0; i--)
    {
      var d = dist(food[i].x, food[i].y, this.position.x, this.position.y);
      if (d < this.maxSpeed && nutrition != 0)
      {
        food.splice(i,1); // remove the i element
        this.health += nutrition;
      }
      else if (d < record && d < perception)
      {
        record = d;
        closest = food[i];
      }
    }

    if (closest != null)
      return this.seek(closest);

    return createVector(0,0);
  }



  this.seek = function(target)
  {
    var desired = p5.Vector.sub(target, this.position);
    desired.setMag(this.maxSpeed);
    var steer = p5.Vector.sub(desired, this.velocity);
    //this.applyForce(steer);
    return steer;
  }

  this.dead = function()
  {
    return (this.health < 0);
  }

  this.display = function()
  {
    // Color based on health
    var green = color(0, 255, 0);
    var red = color(255, 0, 0);
    var col = lerpColor(red, green, this.health)

    // Draw a triangle rotated in the direction of velocity
    var theta = this.velocity.heading() + PI / 2;
    push();
    translate(this.position.x, this.position.y);

    if (debug.checked())
    {
    noFill();
    stroke(0, 255, 0);
    ellipse(0,0,this.dna[2]*2);
    stroke(255, 0, 0);
    ellipse(0,0,this.dna[3]*2);
    stroke(0, 0, 255);
    ellipse(0,0,this.dna[5]*2);
  }
    rotate(theta);

    fill(col);
    stroke(col);
    beginShape();
    vertex(0, -this.r * 2);
    vertex(-this.r, this.r * 2);
    vertex(this.r, this.r * 2);
    endShape(CLOSE);
    pop();
  }

  // A force to keep it on screen
  this.boundaries = function()
  {
    var d = 10;
    var desired = null;
    if (this.position.x < d)
      desired = createVector(this.maxSpeed, this.velocity.y);
    else if (this.position.x > width - d)
      desired = createVector(-this.maxSpeed, this.velocity.y);

    if (this.position.y < d)
      desired = createVector(this.velocity.x, this.maxSpeed);
    else if (this.position.y > height - d)
      desired = createVector(this.velocity.x, -this.maxSpeed);

    if (desired !== null)
    {
      desired.setMag(this.maxSpeed);
      var steer = p5.Vector.sub(desired, this.velocity);
      steer.limit(this.maxForce);
      this.applyForce(steer);
    }
  }
}
