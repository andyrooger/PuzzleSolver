package pushpuzzle.solver.heuristics;

import java.util.Iterator;

import pushpuzzle.common.PuzzleLayout;
import pushpuzzle.common.PuzzleState;
import solver.utility.Coords;

//Sum of shortest distance of each box to any target
public abstract class TraditionalHeuristic implements Heuristic
{
	protected PuzzleLayout layout;
	protected abstract int dist(Coords s, Coords d);
	
	public TraditionalHeuristic(PuzzleLayout layout)
	{
		this.layout = layout;
	}
	
	public int heuristic(PuzzleState state)
	{
		int h = 0;
  	
  	for(Coords c : state.boxes())
  	{
  		int nearest = 0;
  		Iterator<Coords> i = layout.targets().iterator();
  		if(i.hasNext())
  			nearest = dist(i.next(),c);
  		while(i.hasNext())
  		{
  			int n = dist(i.next(),c);
  			if(n < nearest)
  				nearest = n;
  		}
  		h += nearest;
  	}
    return h;
	}
}
