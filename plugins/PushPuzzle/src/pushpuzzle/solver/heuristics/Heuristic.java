package pushpuzzle.solver.heuristics;

import pushpuzzle.common.PuzzleState;

public interface Heuristic
{
	public int heuristic(PuzzleState p);
}
