package pushpuzzle.solver;

import java.util.List;
import java.util.Set;

import pushpuzzle.common.PuzzleState;
import solver.gui.ChoiceDialog;
import solver.utility.ai.AStar;
import solver.utility.ai.AStarProgress;

public abstract class SolverAlgorithm extends AStar<PuzzleState, BoxMove>
{
	private ProgressDialog dialog;
	private int tested;
	private SolverExistence existence;
	private boolean eTest;
	private boolean tTest;
	
	public SolverAlgorithm(ProgressDialog dialog, PushProblem prob)
  {
		super(prob);
		this.dialog = dialog;
		ChoiceDialog<String> tests = new ChoiceDialog<String>(null, "Choose filter tests", true);
		tests.addChoice("Existence", "e");
		tests.addChoice("Terminal", "t");
		Set<String> cTests = tests.getChoices();
		eTest = cTests.contains("e");
		tTest = cTests.contains("t");
		if(eTest)
			existence = new SolverExistence();
		tested = 0;
  }
	
	public void solve()
	{
		super.solve();
	}

  protected void progress(List<AStarProgress> is)
  {
  	tested += is.size();
  	AStarProgress prog = is.get(is.size()-1);
  	dialog.addStatus("Tested "+tested+" moves. Path at "+prog.current+" moves.");
  	dialog.movesLeft(prog.expected);
  }
  
  protected void addState(ReachedState s)
  {
  	if(eTest && !existence.add(s.state()))
  		return;
  	if(tTest && s.move() != null && s.state().terminal(s.move().to()))
  		return;
  	
  	super.addState(s);
  }
}
