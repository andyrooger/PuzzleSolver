package solver.utility.ai;

import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.TreeSet;

import javax.swing.SwingWorker;

import solver.utility.ai.SearchProblem;

public abstract class AStar<State, Move>
{
	protected abstract void aborted();
	protected abstract void solved(List<Move> moves);
	protected abstract void progress(List<AStarProgress> is);
	
	private SearchProblem<State, Move> problem;
	private SwingWorker<List<Move>, AStarProgress> worker;
	private TreeSet<ReachedState> processing;
	
	protected AStar(SearchProblem<State, Move> problem)
	{
		if(problem == null)
			throw new NullPointerException();
		this.problem = problem;
		this.processing = new TreeSet<ReachedState>();
		worker = new Worker();
	}
	
	protected void addState(ReachedState s)
	{
		processing.add(s);
	}
	
	public void solve()
	{
		worker.execute();
	}
	
	public List<Move> solveAndWait()
	{
		worker.execute();
		try
    {
      return worker.get();
    }
  	catch(Exception e)
    {
      e.printStackTrace();
      return null;
    }
	}
	
	public void abort()
	{
		worker.cancel(false);
	}
	
	private class Worker extends SwingWorker<List<Move>, AStarProgress>
	{
    protected List<Move> doInBackground() throws InterruptedException
    {
    	addState(new ReachedState(problem.getInitial(), 0, null, null));
    	while(!processing.isEmpty())
    	{
    		if(isCancelled())
    			throw new InterruptedException();
    		
    		Iterator<ReachedState> i = processing.iterator();
    		ReachedState current = i.next();
    		i.remove();
    		publish(new AStarProgress(current.cost, current.future));
    		
    		if(problem.goal(current.state))
    		{
    			LinkedList<Move> moves = new LinkedList<Move>();
    			
    			while(current.move != null)
    			{
    				moves.addFirst(current.move);
    				current = current.parent;
    			}
    			
    			return moves;
    		}
    		
    		for(Move m : problem.getTransitions(current.state))
    		{
    			State s = problem.applyTransition(m, current.state);
    			int c = current.cost + problem.cost(m);
    			addState(new ReachedState(s, c, m, current));
    		}
    	}
    	
	    return null;
    }
    
    protected void done()
    {
    	try
      {
	      solved(get());
      }
    	catch(Exception e)
      {
      	aborted();
	      e.printStackTrace();
      }
    }
    
    protected void process(List<AStarProgress> is)
    {
    	progress(is);
    }
	}
	
	protected class ReachedState implements Comparable<ReachedState>
	{
		private final State state;
		private final int cost;
		private final int future;
		private final Move move;
		private final ReachedState parent;
		
		public ReachedState(State s, int c, Move m, ReachedState p)
		{
			state = s;
			cost = c;
			future = problem.heuristic(state);
			move = m;
			parent = p;
		}
		
		private int expectedCost()
		{
			return cost + future;
		}
		
		public State state()
		{
			return state;
		}
		
		public Move move()
		{
			return move;
		}
		
		public ReachedState from()
		{
			return parent;
		}

    public int compareTo(ReachedState rs)
    {
    	int cc = new Integer(expectedCost()).compareTo(rs.expectedCost());
	    if(cc != 0)
	    	return cc;
	    
    	int sc = problem.compare().compare(state, rs.state);
    	return sc;
    }
	}
}