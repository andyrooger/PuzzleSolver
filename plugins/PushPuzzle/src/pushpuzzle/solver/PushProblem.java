package pushpuzzle.solver;

import java.util.Comparator;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;

import pushpuzzle.common.GridPuzzle;
import pushpuzzle.common.IllegalMoveException;
import pushpuzzle.common.PuzzleState;
import pushpuzzle.solver.heuristics.Heuristic;
import pushpuzzle.solver.heuristics.HungarianHeuristic;
import pushpuzzle.solver.heuristics.MyHungarianHeuristic;
import pushpuzzle.solver.heuristics.PairedHeuristic;
import pushpuzzle.solver.heuristics.ReversePairedHeuristic;
import pushpuzzle.solver.heuristics.ShiftSumHeuristic;
import pushpuzzle.solver.heuristics.TraditionalManhattan;
import pushpuzzle.solver.heuristics.TraditionalPath;
import solver.gui.ChoiceDialog;
import solver.utility.Coords;
import solver.utility.Direction;
import solver.utility.ai.SearchProblem;

public class PushProblem implements SearchProblem<PuzzleState, BoxMove>
{
	private GridPuzzle puzzle;
	private Heuristic heuristic;
	private int moveCost;
	
	public PushProblem(GridPuzzle puzzle)
	{
		this.puzzle = puzzle;
		ChoiceDialog<Heuristic> hChoice = new ChoiceDialog<Heuristic>(null, "Choose a heuristic", false);
		hChoice.addChoice("Hungarian", new HungarianHeuristic(puzzle));
		hChoice.addChoice("My Hungarian", new MyHungarianHeuristic(puzzle));
		hChoice.addChoice("Paired", new PairedHeuristic(puzzle));
		hChoice.addChoice("Reverse Paired", new ReversePairedHeuristic(puzzle));
		hChoice.addChoice("Shift Sum", new ShiftSumHeuristic(puzzle));
		hChoice.addChoice("Traditional Manhattan", new TraditionalManhattan(puzzle));
		hChoice.addChoice("Traditional Path Finder", new TraditionalPath(puzzle));
		heuristic = hChoice.getChoice();
		
		ChoiceDialog<Integer> iChoice = new ChoiceDialog<Integer>(null, "Which is more important?", false);
		iChoice.addChoice("Optimum Solution", 1);
		iChoice.addChoice("Fast Solution", 0);
		moveCost = iChoice.getChoice();
	}
	
  public PuzzleState applyTransition(BoxMove m, PuzzleState s)
  {
  	try
  	{
  		return s.applyMove(m);
  	}
  	catch(IllegalMoveException e)
  	{
  		return null;
  	}
  }

  public Comparator<PuzzleState> compare()
  {
    return new Comparator<PuzzleState>()
		{
      public int compare(PuzzleState arg0, PuzzleState arg1)
      {
      	Iterator<Coords> i = arg0.boxes().iterator();
      	Iterator<Coords> j = arg1.boxes().iterator();
      	int comparison = 0;
      	while(i.hasNext() && j.hasNext())
      	{
      		comparison = i.next().compareTo(j.next());
      		if(comparison != 0)
      			return comparison;
      	}
      	
      	if(arg0.accessible(arg1.player()))
      		return 0;
      	else
      	{
      		for(Coords c : puzzle.dims())
      		{
      			if(arg0.accessible(c) != arg1.accessible(c))
      			{
      				return (arg0.accessible(c))?1:-1;
      			}
      		}
      	}
      	
      	return 0;
      }
		};
  }

  public int cost(BoxMove m)
  {
  	return moveCost;
  }

  public PuzzleState getInitial()
  {
    return puzzle.current();
  }

  public List<BoxMove> getTransitions(PuzzleState state)
  {
  	List<BoxMove> moves = new LinkedList<BoxMove>();
  	
  	for(Coords box : state.boxes())
  	{
  		Coords n = box.adj(Direction.NORTH);
  		Coords e = box.adj(Direction.EAST);
  		Coords s = box.adj(Direction.SOUTH);
  		Coords w = box.adj(Direction.WEST);
  		
  		if(state.accessible(s) && !puzzle.wall(n) && !state.boxes().contains(n))
  			moves.add(new BoxMove(box, Direction.NORTH));
  		if(state.accessible(n) && !puzzle.wall(s) && !state.boxes().contains(s))
  			moves.add(new BoxMove(box, Direction.SOUTH));
  		if(state.accessible(w) && !puzzle.wall(e) && !state.boxes().contains(e))
  			moves.add(new BoxMove(box, Direction.EAST));
  		if(state.accessible(e) && !puzzle.wall(w) && !state.boxes().contains(w))
  			moves.add(new BoxMove(box, Direction.WEST));
  	}
  	
    return moves;
  }

  public boolean goal(PuzzleState s)
  {
    return s.goal();
  }
  
  public int heuristic(PuzzleState s)
  {
  	return heuristic.heuristic(s);
  }
}