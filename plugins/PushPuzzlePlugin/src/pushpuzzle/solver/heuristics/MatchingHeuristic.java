package pushpuzzle.solver.heuristics;

import java.util.Iterator;
import java.util.Set;

import solver.utility.Coords;

public class MatchingHeuristic
{
	public int heuristic(Set<Coords> set1, Set<Coords> set2)
	{
		// (Assume set1 is boxes and set2 is targets)
		// Distance between each box and target
		// The +1 col is the index to the nearest target
		// The +2 col is the value of the farthest target
		int dists[][] = new int[set1.size()][set2.size()+2];
		
		int farthest = 0;
		
		Iterator<Coords> iSet1 = set1.iterator();
		for(int s1=0; s1<set1.size(); s1++)
		{
			Coords elem1 = iSet1.next();
			Iterator<Coords> iSet2 = set2.iterator();
			int nearest = 0, farthestInd=0;
			for(int s2=0; s2<set2.size(); s2++)
			{
				Coords elem2 = iSet2.next();
				dists[s1][s2] = elem1.manhattanDist(elem2);
				if(dists[s1][s2] < dists[s1][nearest])
					nearest = s2;
				if(dists[s1][s2] > dists[s1][farthestInd])
					farthestInd = s2;
			}
			dists[s1][dists[s1].length-2] = nearest;
			dists[s1][dists[s1].length-1] = dists[s1][farthestInd];
			if(dists[s1][dists[s1].length-1] > farthest)
				farthest = dists[s1][dists[s1].length-1];
		}
		
		
		return sumFarthest(dists, farthest);
	}
	
	private int nearestSet1Index(int[][] dists, int s1)
	{
		return dists[s1][dists[s1].length-2];
	}
	
	private int farthestElem(int[][] dists)
	{
		int farthestS1 = 0;
		for(int s1=0;s1<dists.length;s1++)
		{
			if(dists[s1][nearestSet1Index(dists,s1)] > dists[farthestS1][nearestSet1Index(dists, farthestS1)])
				farthestS1 = s1;
		}
		return farthestS1;
	}
	
	private int sumFarthest(int[][] dists, int farthest)
	{
		// Find index to farthest box
		int farthestElem = farthestElem(dists);
		
		// Distance of farthest box to its nearest target
		int dist = dists[farthestElem][nearestSet1Index(dists, farthestElem)];
		
		// distance of farthest box is zero so all others will be less
		if(dist == 0)
			return 0;
		
		// Stop this box being seen again
		dists[farthestElem][nearestSet1Index(dists, farthestElem)] = 0;
		
		// Stop this target being seen again
		for(int b=0; b<dists.length; b++)
		{
			if(b != farthestElem)
			{
				//Set the target to one more than the old farthest for each box
				dists[b][nearestSet1Index(dists, farthestElem)] = farthest+1;
			}
		}
		
		// update other nearest targets
		for(int s1=0;s1<dists.length;s1++)
		{
			// check if the nearest target is our one
			if(nearestSet1Index(dists, s1) == nearestSet1Index(dists, farthestElem))
			{
				if(s1 != farthestElem)
				{
					int near = 0;
					for(int s2=0; s2<dists[s1].length-2; s2++)
					{
						if(dists[s1][s2] < dists[s1][near])
							near = s2;
					}
					dists[s1][dists[s1].length-2] = near;
				}
			}
		}
		
		return dist + sumFarthest(dists, farthest);
	}
}
