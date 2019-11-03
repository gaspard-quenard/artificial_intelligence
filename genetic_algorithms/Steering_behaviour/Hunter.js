

var Hunter = function(x, y)
{
  this.acceleration = createVector(0,0);
  this.velocity = createVector(0, -2);
  this.position = createVector(x,y);
  this.r = 20;
  this.maxSpeed = 3;
  this.maxForce = 0.5;

  this.update = function()
  {
    this.velocity.add(this.acceleration);
    this.velocity.limit(this.maxSpeed);
    this.position.add(this.velocity);
    this.acceleration.mult(0);
  }

  this.applyForce = function(force)
  {
      this.acceleration.add(force);
  }

  this.hunt = function(vehicles)
  {
      var record = Infinity;
      var closestIndex = -1;

      for (var i = vehicles.length -1; i >= 0; i--)
      {
        var d = dist(vehicles[i].position.x, vehicles[i].position.y, this.position.x, this.position.y);
        if (d < this.r/2)
        {
          this.r += 1;
          this.maxSpeed -= 0.02;
          vehicles.splice(i,1); // remove the i element
        }
        else if (d < record)
        {
          record = d;
          closestIndex = i;
        }
      }

      if (vehicles[closestIndex] != null)
      {
        var force = this.seek(vehicles[closestIndex]);
        this.applyForce(force);
      }
      else
        this.applyForce(0);
  }


  this.seek = function(target)
  {
    var desired = p5.Vector.sub(target.position, this.position);
    desired.setMag(this.maxSpeed);
    var steer = p5.Vector.sub(desired, this.velocity);
    //this.applyForce(steer);
    return steer;
  }

  this.display = function()
  {
    fill(0, 100, 255);
    ellipse(this.position.x,this.position.y,this.r/2);
  }
}
