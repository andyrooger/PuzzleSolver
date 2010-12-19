package pushpuzzle.common;

import java.io.Serializable;
import java.util.TreeSet;

import solver.utility.Coords;

public class DeadSpot implements Serializable
{
	public static final long serialVersionUID = 1;
	
	private final TreeSet<Coords> coords;
	private final int targets;
	
	public DeadSpot(TreeSet<Coords> coords, TreeSet<Coords> targets)
	{
		this.coords = coords;
		
		this.targets = containsBoxes(targets);
	}
	
	public int targets()
	{
		return targets;
	}
	
	public TreeSet<Coords> coords()
	{
		return coords;
	}
	
	public boolean containsBox(Coords box)
	{
		return coords.contains(box);
	}
	
	public int containsBoxes(TreeSet<Coords> boxes)
	{
		TreeSet<Coords> containedTargets = new TreeSet<Coords>(coords);
		containedTargets.retainAll(boxes);
		
		return containedTargets.size();
	}
	
	public String toString()
	{
		String s = "";
		for(Coords c : coords)
			s += c + ", ";
		return s;
	}
}
