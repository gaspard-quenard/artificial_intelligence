
var board;
var population;

var compteurFrame = 0;
var compteur = 0;
var fileLevel  = '';

//chaque bloc fait 40 pixel de largeur et de hauteur

function preload()
{
  fileLevel = loadStrings("./Levels/level4");
}

function setup()
{
  createCanvas(40*parseInt(fileLevel[0]), 40*parseInt(fileLevel[1]));
  board = new plateau(fileLevel);
  population = new population();
}

function draw()
{
  compteurFrame++;
  if (compteurFrame%4 === 0)
  {
    compteur++;
    if (compteur === population.lifespanPop)
    {
      //this.population.optimize()
      //console.log(population.caracters[0].historyPosition)
      population.evaluate(board);
      population.selection();
      compteur = 0;
    }
    background(180,180,180);
    population.run(board);
    board.draw();

  }
}
