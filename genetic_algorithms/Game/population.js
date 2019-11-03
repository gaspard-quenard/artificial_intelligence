


var population = function()
{
  this.caracters = [];
  this.popsize = 1000;
  this.lifespanPop = 100;
  this.factorMutation = 0.03;
  this.matingPool = [];
  this.DnaBestInPop;

  for (var i = 0; i < this.popsize; i++)
    this.caracters[i] = new caracter(this.lifespanPop);

  this.run = function(plateau)
  {
    for (var i = 0; i < this.popsize; i++)
    {
      this.caracters[i].update(plateau);
      this.caracters[i].draw();
    }
  }

  this.evaluate = function(plateau)
  {
    var maxFitness = 0;

    for (var i = 0; i < this.popsize; i++)
    {
      this.caracters[i].calcFitness(plateau);
      if (this.caracters[i].fitness > maxFitness)
      {
        maxFitness = this.caracters[i].fitness;
        this.DnaBestInPop = this.caracters[i].dna;
      }
    }


    for (var i = 0; i < this.popsize; i++)
      this.caracters[i].fitness /= maxFitness;

      this.matingPool = [];

    for (var i = 0; i < this.popsize; i++)
    {
      var n = this.caracters[i].fitness * 100;
      for (var j = 0; j < Math.floor(n); j++)
         this.matingPool.push(this.caracters[i]);
    }
  }

  this.selection = function()
  {
     var newCaracters = [];
     //print(this.matingPool.length)
     print(Math.floor(9/10*this.caracters.length))
     for (var i = 0; i < Math.floor(9/10*this.caracters.length); i++)
     {
       var parentA = random(this.matingPool).dna;
       var parentB = random(this.matingPool).dna;
       var child = this.crossover(parentA, parentB);
       this.mutation(child);
       newCaracters[i] = new caracter(this.lifespanPop, child);
     }
     for (var i = Math.floor(9/10*this.caracters.length); i < this.caracters.length; i++)
      newCaracters[i] = new caracter(this.lifespanPop, this.DnaBestInPop);

     this.caracters = newCaracters;
  }


  this.optimize = function()
  {
      for (var i = 0; i < this.caracters.length; i++)
        this.caracters[i].optimize();
  }


  this.crossover = function(dnaParentA, dnaParentB)
  {
    var newdna = [];
    for (var i = 0; i < dnaParentA.length; i++)
    {
      if (random() < 0.5)
        newdna[i] = dnaParentA[i];
      else
        newdna[i] = dnaParentB[i];
    }
    return newdna
  }

  this.mutation = function(dnaChild)
  {
    for (var i = 0; i < dnaChild.length; i++)
    {
      if (random() < this.factorMutation)
        dnaChild[i] = Math.floor(random(0, 3));
    }
  }
}
