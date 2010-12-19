package pushpuzzle.solver.heuristics;

import pushpuzzle.common.PuzzleLayout;
import solver.utility.Coords;

public class TraditionalManhattan extends TraditionalHeuristic
{
	public TraditionalManhattan(PuzzleLayout layout)
	{
		super(layout);
	}
	
	protected int dist(Coords s, Coords d)
	{
		return s.manhattanDist(d);
	}
}
