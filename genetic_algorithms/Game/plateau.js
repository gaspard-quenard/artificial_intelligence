


var plateau = function(fileLevel)
{
  // outputs the content of the text file

  console.log("Width : ", fileLevel[0]);
  console.log("Height : ", fileLevel[1]);

  this.width = parseInt(fileLevel[0]);
  this.height = parseInt(fileLevel[1]);
  this.goal = createVector(this.width-2,this.height-2);
  this.board = [];

  for (var i = 0; i < this.width; i++)
    this.board[i] = [];


  for (var i = 0; i < this.width; i++)
    for (var j = 0; j < this.height; j++)
    {
      if (parseInt(fileLevel[2+j][2*i]) === 1)
        this.board[i][j] = true;
      else
        this.board[i][j] = false;
    }


  this.draw = function()
  {
    fill(color(255,255,255))
    for (var i = 0; i < this.width; i++)
      for (var j = 0; j < this.height; j++)
        if (this.board[i][j] === true)
          rect(i*40, j*40, 40, 40);

    fill(color(0, 0, 255))
    ellipse(this.goal.x*40 + 20,this.goal.y*40 + 20, 40)
  }
}
