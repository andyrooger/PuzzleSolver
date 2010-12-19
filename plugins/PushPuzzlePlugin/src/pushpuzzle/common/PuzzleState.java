package pushpuzzle.common;

import java.io.Serializable;
import java.util.TreeSet;

import pushpuzzle.solver.BoxMove;
import solver.utility.BoolMap;
import solver.utility.Coords;
import solver.utility.Direction;

public class PuzzleState implements Serializable
{
	public static final long serialVersionUID = 1;
	
	private final PuzzleLayout pLayout;
	private final TreeSet<Coords> boxes;
	private final Coords player;
	private final BoolMap accessibility;
	
	public PuzzleState(PuzzleLayout layout, TreeSet<Coords> boxes, Coords player) throws PuzzleCreateException
	{
		if(layout == null)
			throw new PuzzleCreateException("No puzzle layout given");
		this.pLayout = layout;
		if(boxes == null)
			throw new PuzzleCreateException("No boxes given");
		this.boxes = boxes;
		if(player == null)
			throw new PuzzleCreateException("No player given");
		this.player = player;
		
		accessibility = getAccessibility();
	}
	
	public TreeSet<Coords> boxes()
	{
		return boxes;
	}
	
	public Coords player()
	{
		return player;
	}
	
	public boolean accessible(Coords c)
	{
		return accessibility.get(c);
	}
	
	public BoolMap accessibility()
	{
		return accessibility;
	}
	
	public boolean goal()
	{
		TreeSet<Coords> targets = new TreeSet<Coords>(pLayout.targets());
		targets.removeAll(boxes());
		
		return (targets.size() == 0);
	}
	
	public boolean terminal(Coords box)
	{
		DeadSpot horiz = pLayout.horizDead(box);
		DeadSpot vert = pLayout.vertDead(box);
		
		if(horiz == null && vert == null)
			return false;
		
		if(horiz != null && vert != null)
			return !pLayout.targets().contains(box);
		
		DeadSpot intersect = (horiz == null)?vert:horiz;
		int ts = intersect.targets();
		int bs = intersect.containsBoxes(boxes);
		
		return (ts < bs);
	}
	
	private BoolMap getAccessibility()
	{
		BoolMap acc = new BoolMap(pLayout.dims(), false);
		recurseAccess(acc, player);
		return acc;
	}
	
	private void recurseAccess(BoolMap am, Coords pos)
	{
		if(!pLayout.wall(pos) && !boxes.contains(pos) && !am.get(pos))
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
	
	public PuzzleState applyMove(BoxMove move) throws IllegalMoveException
	{
		TreeSet<Coords> nBoxes = new TreeSet<Coords>(boxes);
		
  	if(!nBoxes.remove(move.box()))
  		throw new IllegalMoveException();
  	
  	nBoxes.add(move.to());
  	try
  	{
  		return new PuzzleState(pLayout, nBoxes, move.box());
  	}
  	catch(PuzzleCreateException e)
  	{
  		return null;
  	}
	}
}
