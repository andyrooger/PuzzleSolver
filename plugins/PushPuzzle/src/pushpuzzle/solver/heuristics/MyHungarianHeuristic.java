package pushpuzzle.solver.heuristics;

import java.util.Iterator;
import java.util.Set;

import pushpuzzle.common.PuzzleLayout;
import pushpuzzle.common.PuzzleState;
import solver.utility.Coords;

public class MyHungarianHeuristic implements Heuristic
{
	private final PuzzleLayout layout;
	
	public MyHungarianHeuristic(PuzzleLayout layout)
	{
		this.layout = layout;
	}
	
	public int heuristic(PuzzleState p)
  {
  	int[][] costs = getCosts(p.boxes(), layout.targets());
  	reduceCosts(costs);
  	//AssignmentProblem prob = new AssignmentProblem(costs);
  	//int[][] indices = prob.solve(new HungarianAlgorithm());
  	
  	//float tot = 0;
  	//for(int[] ind : indices)
  	//	tot += costs[ind[0]][ind[1]];
  	
	  //return (int)tot;
  	return 0;
  }
  
  private int[][] getCosts(Set<Coords> agents, Set<Coords> activities)
	{
		int[][] costs = new int[activities.size()][agents.size()];
		
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
	
  private void reduceCosts(int[][] costs)
  {
  	if(costs.length <= 0)
  		return;
  	
  	for(int i=0;i<costs.length;i++)
  	{
  		int min = 0;
  		for(int j=0;j<costs[i].length;j++)
  			if(costs[i][j]<min)
  				min = costs[i][j];
  		for(int j=0;j<costs[i].length;j++)
  			costs[i][j] -= min;
  	}
  	
  	for(int j=0;j<costs[0].length;j++)
  	{
  		int min = 0;
  		for(int i=0;i<costs.length;i++)
  			if(costs[i][j]<min)
  				min = costs[i][j];
  		for(int i=0;i<costs.length;i++)
  			costs[i][j] -= min;
  	}
  }
}
