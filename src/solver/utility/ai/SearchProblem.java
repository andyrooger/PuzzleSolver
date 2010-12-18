package solver.utility.ai;

import java.util.Comparator;
import java.util.List;

public interface SearchProblem<State, Move>
{
	public State getInitial();
	public List<Move> getTransitions(State s);
	public State applyTransition(Move m, State s);
	public int heuristic(State s);
	public boolean goal(State s);
	public int cost(Move m);
	public Comparator<State> compare();
}
