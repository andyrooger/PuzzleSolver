package pushpuzzle.solver.heuristics;

import java.util.Iterator;
import java.util.Set;

import pushpuzzle.common.PuzzleLayout;
import pushpuzzle.common.PuzzleState;
import pushpuzzle.solver.heuristics.notmine.AssignmentProblem;
import pushpuzzle.solver.heuristics.notmine.HungarianAlgorithm;
import solver.utility.Coords;

public class HungarianHeuristic implements Heuristic
{
	private final PuzzleLayout layout;
	
	public HungarianHeuristic(PuzzleLayout layout)
	{
		this.layout = layout;
	}
	
  public int heuristic(PuzzleState p)
  {
  	float[][] costs = getCosts(p.boxes(), layout.targets());
  	AssignmentProblem prob = new AssignmentProblem(costs);
  	int[][] indices = prob.solve(new HungarianAlgorithm());
  	
  	float tot = 0;
  	for(int[] ind : indices)
  		tot += costs[ind[0]][ind[1]];
  	
	  return (int)tot;
  }
  
  private float[][] getCosts(Set<Coords> agents, Set<Coords> activities)
	{
		float[][] costs = new float[activities.size()][agents.size()];
		
		Iterator<Coords> activityI = activities.iterator();
		for(int x=0; x<costs.length; x++)
		{
			Coords activity = activityI.next();
			Iterator<Coords> agentI = agents.iterator();
			for(int y=0; y<costs[x].length; y++)
				costs[x][y] = agentI.next().manhattanDist(activity);
		}
		
		return costs;
	}
}


/*
import java.util.Arrays;

import java.util.Iterator;
import java.util.Set;

import pushpuzzle.common.PuzzleLayout;
import pushpuzzle.common.PuzzleState;
import solver.utility.Coords;

public class HungarianHeuristic implements Heuristic
{
	private final PuzzleLayout layout;
	
	public HungarianHeuristic(PuzzleLayout layout)
	{
		this.layout = layout;
	}
	
	public int heuristic(PuzzleState p)
	{
		int[][] costs = getCosts(p.boxes(), layout.targets());
		
		reduceCosts(costs);
		
		int[] coveredRows = new int[p.boxes().size()];
		int[] coveredCols = new int[layout.targets().size()];
		int lines = cover(costs, coveredRows, coveredCols);
		while(lines != p.boxes().size())
		{
			lines = cover(costs, coveredRows, coveredCols);
		}
		
		return 0;
	}
	
	private int[][] getCosts(Set<Coords> agents, Set<Coords> activities)
	{
		int[][] costs = new int[activities.size()][agents.size()];
		
		Iterator<Coords> activity = activities.iterator();
		for(int x=0; x<costs.length; x++)
		{
			Iterator<Coords> agent = agents.iterator();
			for(int y=0; y<costs[x].length; y++)
				costs[x][y] = agent.next().manhattanDist(activity.next());
		}
		
		return costs;
	}
	
	private void reduceCosts(int[][] costs)
	{
		for(int x=0; x<costs.length; x++)
		{
			int least = 0;
			for(int y=0; y<costs[x].length; y++)
			{
				if(costs[x][y] < costs[x][least])
					least = y;
			}
			
			for(int y=0; y<costs[x].length; y++)
				costs[x][y] -= costs[x][least];
		}
		
		for(int y=0; y<costs[0].length; y++)
		{
			int least = 0;
			for(int x=0; x<costs.length; x++)
			{
				if(costs[x][y] < costs[least][y])
					least = x;
			}
			
			for(int x=0; x<costs.length; x++)
				costs[x][y] -= costs[least][y];
		}
	}
	
	private int cover(int[][] costs, int[] coveredRows, int[] coveredCols)
	{
		int lines = 0;
		Arrays.fill(coveredRows, 0);
		Arrays.fill(coveredCols, 0);
		
		return 0;
	}
}

*/