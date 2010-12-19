package pushpuzzle.common;

import java.util.TreeSet;

import solver.utility.BoolMap;
import solver.utility.Coords;
import solver.utility.Dimensions;

public interface PuzzleLayout
{
	public Dimensions dims();
	public boolean wall(Coords c);
	public BoolMap accessibility();
	public TreeSet<Coords> targets();
	public DeadSpot horizDead(Coords box);
	public DeadSpot vertDead(Coords box);
}
