package solver.utility;

import java.io.Serializable;

public class Coords implements Comparable<Coords>, Serializable
{
	public static final long serialVersionUID = 1;
	
	private final int row, col;
	
	public Coords(int row, int col)
	{
		this.row = row;
		this.col = col;
	}
	
	public int getRow()
	{
		return row;
	}
	
	public int getCol()
	{
		return col;
	}
	
	public Coords adj(Direction d)
	{
		switch(d)
		{
			case EAST:
				return new Coords(row, col+1);
			case NORTH:
				return new Coords(row-1, col);
			case SOUTH:
				return new Coords(row+1, col);
			case WEST:
				return new Coords(row, col-1);
			default:
				return this;
		}
	}
	
	public boolean equals(Coords c)
	{
		if(c == null)
			return false;
		return (c.col == col && c.row == row);
	}
	
	public int manhattanDist(Coords c)
	{
		int x = c.col - col;
		if(x < 0)
			x = -x;
		int y = c.row - row;
		if(y < 0)
			y = -y;
		return x+y;
	}

  public int compareTo(Coords c)
  {
  	if(row > c.row)
  		return 1;
  	else if(row < c.row)
  		return -1;
  	else if(col > c.col)
  		return 1;
  	else if(col < c.col)
  		return -1;
  	else return 0;
  }
  
  public String toString()
  {
  	return "("+col+", "+row+")";
  }
}
