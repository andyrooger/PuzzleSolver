package pushpuzzle.common;

import java.io.Serializable;
import java.util.LinkedList;
import java.util.List;
import java.util.TreeSet;

import solver.plugin.IPuzzle;
import solver.utility.BoolMap;
import solver.utility.Coords;
import solver.utility.Dimensions;
import solver.utility.Direction;

public class GridPuzzle implements IPuzzle, PuzzleLayout
{
	public static final long serialVersionUID = 1;
	
	private PuzzleState initialState;
	private LinkedState state;
	private final BoolMap walls;
	private final TreeSet<Coords> targets;
	private final BoolMap accessibility;
	private final List<DeadSpot> horizSpots;
	private final List<DeadSpot> vertSpots;
	
	public GridPuzzle(BoolMap walls, TreeSet<Coords> targets, TreeSet<Coords> boxes, Coords player) throws PuzzleCreateException
	{
		if(walls == null)
			throw new PuzzleCreateException("No wall map given");
		if(targets == null)
			throw new PuzzleCreateException("No targets given");
		
		if(walls.dims().getCols() == 0 || walls.dims().getRows() == 0)
			throw new PuzzleCreateException("Invalid wall map: Too small");
		
		this.walls = walls;
		
		for(Coords c : targets)
		{
			if(!walls.dims().contains(c))
				throw new PuzzleCreateException("Invalid target: Out of range");
			if(walls.get(c))
				throw new PuzzleCreateException("Target is under a wall");
		}
		this.targets = targets;
		
		initialState = new PuzzleState(this, boxes, player);
		accessibility = getAccessibility();
		horizSpots = getDeads(true);
		System.out.println("HORIZONTAL SPOTS");
		for(DeadSpot d : horizSpots)
			System.out.println("SPOT: \n"+d.toString());
		vertSpots = getDeads(false);
		restart();
	}
	
	private BoolMap getAccessibility()
	{
		BoolMap acc = new BoolMap(walls.dims(), false);
		recurseAccess(acc, initialState.player());
		return acc;
	}
	
	private void recurseAccess(BoolMap am, Coords pos)
	{
		if(!walls.get(pos) && !am.get(pos))
		{
			am.set(pos, true);
			for(Direction d : Direction.values())
			{
				Coords nc = pos.adj(d);
				if(am.dims().contains(nc))
					recurseAccess(am, nc);
			}
		}
	}
	
	public BoolMap accessibility()
	{
		return accessibility;
	}
	
	private List<DeadSpot> getDeads(boolean horizontal)
	{
		LinkedList<DeadSpot> spots = new LinkedList<DeadSpot>();
		
		// Start terminal spot
		TreeSet<Coords> spot = new TreeSet<Coords>();
		
		// Scan row by row / col by col
		// Look along the row for a floor square with wall above or below
		// Keep adding to a new term spot until this becomes false
		// Add spot to spot pile
		if(horizontal)
		{
			for(int r=-1; r<=dims().getRows(); r++)
				for(int c=-1; c<=dims().getCols(); c++)
					spot = processDeadCell(r, c, spots, spot, Direction.NORTH, Direction.SOUTH);
		}
		else // horizontal == false
		{
			for(int c=-1; c<=dims().getCols(); c++)
				for(int r=-1; r<=dims().getRows(); r++)
					spot = processDeadCell(r, c, spots, spot, Direction.EAST, Direction.WEST);
		}
		
		return spots;
	}
	
	private TreeSet<Coords> processDeadCell(int r, int c, LinkedList<DeadSpot> spots, TreeSet<Coords> spot, Direction dirA, Direction dirB)
	{
		Coords here = new Coords(r, c);
		if(wall(here))
		{
			if(spot != null && !spot.isEmpty())
				spots.add(new DeadSpot(spot, targets));
			
			spot = new TreeSet<Coords>();
		}
		else
		{
			if(wall(here.adj(dirA)) || wall(here.adj(dirB)))
			{
				if(spot != null)
					spot.add(here);
			}
			else
			{
				spot = null;
			}
		}
		
		return spot;
	}
	
	public DeadSpot horizDead(Coords box)
	{
		for(DeadSpot d : horizSpots)
		{
			if(d.containsBox(box))
				return d;
		}
		
		return null;
	}
	
	public DeadSpot vertDead(Coords box)
	{
		for(DeadSpot d : vertSpots)
		{
			if(d.containsBox(box))
				return d;
		}
		
		return null;
	}
	
	public Dimensions dims()
	{
		return walls.dims();
	}
	
	public boolean wall(Coords c)
	{
		return walls.get(c);
	}
	
	public TreeSet<Coords> targets()
	{
		return targets;
	}
	
	public void restart()
	{
		state = new LinkedState(initialState);
	}
	
	public PuzzleState current()
	{
		return state.state;
	}
	
	public void setCurrent(Coords player, TreeSet<Coords> boxes) throws PuzzleCreateException
	{
		LinkedState s = new LinkedState(new PuzzleState(this, boxes, player), null, state.prev);
		if(state.prev != null)
			state.prev.next = s;
		state = s;
	}
	
	public boolean hasNext()
	{
		return (state.next != null);
	}
	
	public PuzzleState next()
	{
		if(state.next != null)
		{
			state = state.next;
			return current();
		}
		else
			return null;
	}
	
	public boolean hasPrevious()
	{
		return (state.prev != null);
	}
	
	public PuzzleState previous()
	{
		if(state.prev != null)
		{
			state = state.prev;
			return current();
		}
		else
			return null;
	}
	
	public void setNext(PuzzleState p)
	{
		state.next = (p == null)?null:(new LinkedState(p, null, state));
	}
	
	public PuzzleState last()
	{
		LinkedState s = state;
		while(s.next != null)
			s = s.next;
		
		return s.state;
	}
	
	public void setLast(PuzzleState p)
	{
		LinkedState s = state;
		while(s.next != null)
			s = s.next;
		
		s.next = (p == null)?null:(new LinkedState(p, null, s));
	}
	
	private class LinkedState implements Serializable
	{
		public static final long serialVersionUID = 1;
		public LinkedState next;
		public PuzzleState state;
		public LinkedState prev;
		
		public LinkedState(PuzzleState s)
		{
			state = s;
			next = null;
			prev = null;
		}
		
		public LinkedState(PuzzleState s, LinkedState n, LinkedState p)
		{
			state = s;
			next = n;
			prev = p;
		}
	}
}
