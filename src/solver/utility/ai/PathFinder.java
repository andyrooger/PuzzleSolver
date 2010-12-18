package solver.utility.ai;

import java.util.Comparator;
import java.util.LinkedList;
import java.util.List;

import solver.utility.BoolMap;
import solver.utility.Coords;
import solver.utility.Direction;

public abstract class PathFinder extends AStar<Coords, Direction>
{
	public PathFinder(BoolMap map, Coords start, Coords finish)
	{
		super(new PathProblem(map, start, finish));
	}

  protected void progress(List<AStarProgress> is)
  {
  	//for(Integer i : is)
  	//	System.out.println("Expected distance to go: "+i);
  }
  
  private static class PathProblem implements SearchProblem<Coords, Direction>
  {
  	private final BoolMap map;
  	private final Coords start, finish;
  	
  	public PathProblem(BoolMap map, Coords start, Coords finish)
  	{
  		if(map == null || start == null || finish == null)
  			throw new NullPointerException();
  		this.map = map;
  		this.start = start;
  		this.finish = finish;
  	}
  	
    public Coords applyTransition(Direction m, Coords s)
    {
	    return s.adj(m);
    }

    public Comparator<Coords> compare()
    {
    	return new Comparator<Coords>()
			{
        public int compare(Coords arg0, Coords arg1)
        {
	        return arg0.compareTo(arg1);
        }
			};
    }

    public int cost(Direction m)
    {
	    return 1;
    }

    public Coords getInitial()
    {
	    return start;
    }

    public List<Direction> getTransitions(Coords s)
    {
    	LinkedList<Direction> dirs = new LinkedList<Direction>();
    	
    	for(Direction d : Direction.values())
    		if(map.get(s.adj(d)))
    			dirs.add(d);
    	
	    return dirs;
    }

    public boolean goal(Coords s)
    {
	    return finish.equals(s);
    }

    public int heuristic(Coords s)
    {
	    return finish.manhattanDist(s);
    }
  }
}