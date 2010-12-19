package pushpuzzle.solver.heuristics;

import pushpuzzle.common.PuzzleLayout;
import pushpuzzle.common.PuzzleState;

public class ReversePairedHeuristic extends MatchingHeuristic implements Heuristic
{
	private PuzzleLayout layout;
	
	public ReversePairedHeuristic(PuzzleLayout layout)
	{
		this.layout = layout;
	}
	
	public int heuristic(PuzzleState p)
	{
		return super.heuristic(layout.targets(), p.boxes());
	}
}
