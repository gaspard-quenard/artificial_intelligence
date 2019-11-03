
function DNA(genes)
{
  
  var magnitude = 0.1;
  
   if (genes)
     this.genes = genes;
   else
   {
     this.genes = []; 
     for (var i = 0; i < lifespan; i++)
     {
         this.genes[i] = p5.Vector.random2D();
         this.genes[i].setMag(magnitude);
     }
   }
   
   this.crossover = function(partner)
   {
     var newdna = [];
     var mid = floor(random(this.genes.length));
     for (var i = 0; i < this.genes.length; i++)
     {
        if (i > 0)
        {
           newdna[i] = this.genes[i]; 
        }
        else
        {
            newdna[i] = partner.genes[i];
        }
     }
     return new DNA(newdna);
   }
   
   this.mutation = function()
   {
     for (var i = 0; i < this.genes.length; i++)
     {
        if (random(1) < 0.01)
        {
           this.genes[i] = p5.Vector.random2D(); 
           this.genes[i].setMag(magnitude);
        }
     }
   }
}
