

var caracter = function(lifespan, dna)
{
  this.width = 10;
  this.height = 10;
  this.positionX = 0;
  this.positionY = 0;
  this.dna = [];
  this.saut = 0;
  this.count = 0;
  this.fitness = 0;
  this.speedArrive = 0;
  this.lifespan = lifespan;
  this.historyPosition = []

  if (dna === undefined)
  {
    for (var i = 0; i < this.lifespan; i++)
      this.dna[i] = Math.floor(random(0, 3))
  }
  else
    this.dna = dna

  this.historyPosition.push(createVector(this.positionX,this.positionY));




  this.update = function(plateau)
  {

    this.fall(plateau);
    this.move(this.dna[this.count], plateau);
    if (dist(this.positionX, this.positionY, plateau.goal.x, plateau.goal.y) === 0
   && this.speedArrive === 0)
   {
     this.speedArrive = this.count;
   }
    this.count++;
    this.historyPosition.push(createVector(this.positionX,this.positionY));
  }


  this.fall = function(plateau)
  {
    if (this.positionY === plateau.height-1)
    {
      this.positionX = 0;
      this.positionY = 0;
    }

    else if (this.saut > 0
    && this.positionY > 0
    && plateau.board[this.positionX][this.positionY-1] === false )
    {
      this.positionY--
      this.saut--;
    }
    else if (plateau.board[this.positionX][this.positionY+1] === false)
    {
      this.positionY++;
    }
  }

  this.move = function(direction, plateau)
  {
    if (direction === 0  // UP
      && plateau.board[this.positionX][this.positionY+1] === true
      && this.positionY > 0
      && plateau.board[this.positionX][this.positionY-1] === false)
    {
      this.saut = 3
    }
    else if (direction === 1  // RIGHT
      && this.positionX < plateau.width-1
      && plateau.board[this.positionX+1][this.positionY] === false)
    {
      this.positionX++;
    }
    else if (direction === 2  // LEFT
      && this.positionX > 0
      && plateau.board[this.positionX-1][this.positionY] === false)
    {
      this.positionX--;
    }
  }


  this.optimize = function()
  {
    //console.log("Initial history : ", this.historyPosition.slice())
    //console.log("Initial dna : ", this.dna.slice())
    for (var i = 0; i < this.historyPosition.length; i++)
    {
      //console.log("On cherche : ", this.historyPosition[i])
      //console.log("On trouve : ", i, this.lastIndex(i, this.historyPosition))
      var lastIndex = this.lastIndex(i, this.historyPosition);
      if (lastIndex != -1)
      {

        this.dna.splice(i, lastIndex);
        this.historyPosition.splice(i, lastIndex);
        //print(this.dna.length)
        //console.log("NEW history : ", this.historyPosition.slice());
        //console.log("NEW dna : ", this.dna.slice());
      }
    }
    while(this.dna.length != this.lifespan)
      this.dna.push(Math.floor(random(0, 3)))
  }


  this.lastIndex = function(pos, array)
  {
    for (var i = array.length-1; i > pos; i--)
    {
      if (array[i].x === array[pos].x && array[i].y === array[pos].y)
        return i
    }
    return -1;
  }


  this.calcFitness = function(plateau)
  {
    var d = dist(this.positionX, this.positionY, plateau.goal.x, plateau.goal.y)
    if (d === 0)
      d = 0.5
    this.fitness = 1 / (pow(d, 4));
    if (this.speedArrive != 0)
      this.fitness *= (this.lifespan - this.speedArrive)
  }


  this.draw = function()
  {
    fill(color(0, 255, 0))
    rect(this.positionX*40, this.positionY*40, 40, 40);
  }
}
