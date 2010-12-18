package solver.plugin;

import solver.gui.PuzzleMode;

public interface IPuzzleType
{
	public String getType(); // String version of the puzzle type
	public IPuzzlePane get(PuzzleMode modej); // get pane for specified mode
}
