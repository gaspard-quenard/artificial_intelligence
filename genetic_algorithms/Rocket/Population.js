function Population()
{
   this.rockets = []; 
   this.popsize = 200;
   this.matingPool = [];
   
   for (var i = 0; i < this.popsize; i++)
   {
     this.rockets[i] = new Rocket();
   }
   
   this.run = function()
   {
      for (var i = 0; i < this.popsize; i++)
      {
         this.rockets[i].update();
         this.rockets[i].show();
      }      
   }
   
   this.evaluate = function()
   {
      var maxFitness = 0;
      for (var i = 0; i < this.popsize; i++)
      {
         this.rockets[i].calcFitness();
         if (this.rockets[i].fitness > maxFitness)
           maxFitness = this.rockets[i].fitness;
         
      } 
      
      for (var i = 0; i < this.popsize; i++)
      {
         this.rockets[i].fitness /= maxFitness;  
      }  
      
      this.matingPool = [];
      
      for (var i = 0; i < this.popsize; i++)
      {
        var n = this.rockets[i].fitness * 100;
         for (var j = 0; j < n; j++)
           this.matingPool.push(this.rockets[i]);
      } 
   }
   
   this.selection = function()
   {
      var newRockets = [];
      for (var i = 0; i < this.rockets.length; i++)
      {
        var parentA = random(this.matingPool).dna;
        var parentB = random(this.matingPool).dna;
        var child = parentA.crossover(parentB);
        child.mutation();
        newRockets[i] = new Rocket(child);
      }
      this.rockets = newRockets;
   }
}
