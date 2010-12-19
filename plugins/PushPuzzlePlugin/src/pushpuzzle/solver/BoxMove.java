package pushpuzzle.solver;

import solver.utility.Coords;
import solver.utility.Direction;

public class BoxMove
{
	private Coords box;
	private Direction dir;
	
	public BoxMove(Coords box, Direction dir)
  {
	  this.box = box;
	  this.dir = dir;
  }

	public Coords box()
  {
  	return box;
  }

	public Direction direction()
  {
  	return dir;
  }
	
	public Coords to()
	{
		return box.adj(dir);
	}
}
