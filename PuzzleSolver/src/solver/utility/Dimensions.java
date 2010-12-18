package solver.utility;

import java.io.Serializable;
import java.util.Iterator;
import java.util.NoSuchElementException;


public class Dimensions implements Iterable<Coords>, Serializable
{
	public static final long serialVersionUID = 1;
	
	private final int rows, cols;
	
	public Dimensions(int rows, int cols)
	{
		this.rows = rows;
		this.cols = cols;
	}
	
	public int getRows()
	{
		return rows;
	}
	
	public int getCols()
	{
		return cols;
	}
	
	public boolean contains(Coords c)
	{
		return (c.getCol() >= 0 && c.getCol() < cols && c.getRow() >= 0 && c.getRow() < rows);
	}

  public Iterator<Coords> iterator()
  {
  	return new Iterator<Coords>()
		{
  		private Coords current = null;
  		
      public boolean hasNext()
      {
      	if(rows < 1 || cols < 1)
      		return false;
      	
	      return (current == null || !current.equals(new Coords(rows-1, cols-1)));
      }

      public Coords next()
      {
      	if(current == null)
      	{
      		if(rows < 1 || cols < 1)
      			throw new NoSuchElementException();
      		
      		current = new Coords(0, 0);
      		return current;
      	}
      	
      	int nrow = current.getRow();
      	int ncol = current.getCol()+1;
      	
      	if(ncol < cols)
      		current = new Coords(nrow, ncol);
      	else
      	{
      		ncol = 0;
      		nrow++;
      		if(nrow < rows)
      			current = new Coords(nrow, ncol);
      		else
      			current = null;
      	}
      	
      	if(current == null)
      		throw new NoSuchElementException();
      	else
      		return current;
      }

      public void remove()
      {
      }
		};
  }
}
