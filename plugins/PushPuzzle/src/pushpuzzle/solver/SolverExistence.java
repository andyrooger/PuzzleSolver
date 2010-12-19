package pushpuzzle.solver;

import java.util.LinkedList;
import java.util.Map;
import java.util.TreeMap;

import pushpuzzle.common.PuzzleState;
import solver.utility.Coords;

public class SolverExistence
{
	private Map<Coords, SolverExistence> split;
	
	public SolverExistence()
	{
		split = new TreeMap<Coords, SolverExistence>();
	}
	
	private LinkedList<Coords> dissect(PuzzleState state)
	{
		LinkedList<Coords> coords = new LinkedList<Coords>(state.boxes());
		
		for(Coords c : state.accessibility().dims())
		{
			if(state.accessible(c))
			{
				coords.add(c);
				break;
			}
		}
		return coords;
	}
	
	public boolean add(PuzzleState state)
	{
		return add(dissect(state));
	}
	
	private boolean add(LinkedList<Coords> coords)
	{
		if(coords.isEmpty())
			return false;
		
		Coords coord = coords.removeFirst();
		SolverExistence child = split.get(coord);
		
		if(child != null)
			return child.add(coords);
		
		child = new SolverExistence();
		split.put(coord, child);
		child.add(coords);
		
		return true;
	}
}
