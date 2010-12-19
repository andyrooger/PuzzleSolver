package pushpuzzle.solver.heuristics;

import java.util.List;

import pushpuzzle.common.PuzzleLayout;
import solver.utility.Coords;
import solver.utility.Direction;
import solver.utility.ai.PathFinder;

public class TraditionalPath extends TraditionalHeuristic
{
	public TraditionalPath(PuzzleLayout layout)
	{
		super(layout);
	}
	
	protected int dist(Coords s, Coords d)
	{
		PathFinder finder = new PathFinder(layout.accessibility(), s, d)
		{
			protected void solved(List<Direction> moves)
			{
			}
			
			protected void aborted()
			{
			}
		};
		List<Direction> moves = finder.solveAndWait();
		
		if(moves == null)
			return s.manhattanDist(d);
		else
			return moves.size();
	}
	
}
