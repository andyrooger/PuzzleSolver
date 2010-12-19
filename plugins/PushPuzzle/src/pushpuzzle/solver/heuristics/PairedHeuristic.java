package pushpuzzle.solver.heuristics;

import pushpuzzle.common.PuzzleLayout;
import pushpuzzle.common.PuzzleState;

public class PairedHeuristic extends MatchingHeuristic implements Heuristic
{
	private PuzzleLayout layout;
	
	public PairedHeuristic(PuzzleLayout layout)
	{
		this.layout = layout;
	}
	
	public int heuristic(PuzzleState p)
	{
		return super.heuristic(p.boxes(), layout.targets());
	}
}
