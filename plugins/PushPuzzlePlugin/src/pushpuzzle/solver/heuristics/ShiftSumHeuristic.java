package pushpuzzle.solver.heuristics;

import java.util.Comparator;
import java.util.Iterator;
import java.util.TreeSet;

import pushpuzzle.common.PuzzleLayout;
import pushpuzzle.common.PuzzleState;
import solver.utility.Coords;

// Take each dimension separately
// Sum the total shift needed
// So start on box at one end, add shift to get to first target.
// Now ignore both of these, and go again
public class ShiftSumHeuristic implements Heuristic
{
	protected PuzzleLayout layout;
	
	public ShiftSumHeuristic(PuzzleLayout layout)
	{
		this.layout = layout;
	}
	
	public int heuristic(PuzzleState state)
	{
		TreeSet<Coords> boxes = new TreeSet<Coords>(new VertCompare());
		boxes.addAll(state.boxes());
		TreeSet<Coords> targets = new TreeSet<Coords>(new VertCompare());
		targets.addAll(layout.targets());
		
		Iterator<Coords> box = boxes.iterator();
		Iterator<Coords> target = targets.iterator();
		
		int h = 0;
		
		while(box.hasNext() && target.hasNext())
			h += abs(box.next().getRow() - target.next().getRow());
		
		boxes = new TreeSet<Coords>(new HorizCompare());
		boxes.addAll(state.boxes());
		targets = new TreeSet<Coords>(new HorizCompare());
		targets.addAll(layout.targets());
		
		box = boxes.iterator();
		target = targets.iterator();
		
		while(box.hasNext() && target.hasNext())
			h += abs(box.next().getCol() - target.next().getCol());
		
		return h;
	}
	
	private int abs(int i)
	{
		return (i < 0)?-i:i;
	}
	
	private class VertCompare implements Comparator<Coords>
	{
    public int compare(Coords arg0, Coords arg1)
    {
    	return new Integer(arg0.getRow()).compareTo(arg1.getRow());
    }
	}
	
	private class HorizCompare implements Comparator<Coords>
	{
    public int compare(Coords arg0, Coords arg1)
    {
    	return new Integer(arg0.getCol()).compareTo(arg1.getCol());
    }
	}
}
