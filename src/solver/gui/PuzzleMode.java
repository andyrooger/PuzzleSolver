package solver.gui;

public enum PuzzleMode
{
	CREATE,
	PLAY;
	
	public String toString()
	{
		String lower = super.toString();
		return lower.substring(0, 1).toUpperCase() + lower.substring(1).toLowerCase();
	}
}
