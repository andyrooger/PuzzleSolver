package pushpuzzle.solver;

import java.awt.Frame;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.List;

import javax.swing.JOptionPane;
import javax.swing.SwingUtilities;

import pushpuzzle.common.GridPuzzle;
import pushpuzzle.common.IllegalMoveException;
import pushpuzzle.player.PushPlayer;
import solver.gui.SolverButton;
import solver.plugin.ISolver;

public class PushSolver implements ISolver
{
	private PushPlayer gui;
	private SolverButton solverBtn;
	private SolverAlgorithm solverAlg;
	
	public PushSolver(PushPlayer gui, SolverButton b)
	{
		this.gui = gui;
		solverBtn = b;
	}
	
	public void start()
	{
		GridPuzzle puzzle = (GridPuzzle)gui.getPuzzle();
		
		PushProblem prob = new PushProblem(puzzle);
		
		int maxProg = (puzzle.dims().getCols()-1) *
									(puzzle.dims().getRows()-1) *
									puzzle.current().boxes().size();
		final WeightedProgressDialog prog = new WeightedProgressDialog((Frame)gui.getTopLevelAncestor(), new ActionListener()
		{
			public void actionPerformed(ActionEvent arg0)
			{
				solverBtn.setSelected(false);
			}
		}, maxProg, prob.heuristic(prob.getInitial()));
		
		solverAlg = new SolverAlgorithm(prog, prob)
		{
			protected void solved(List<BoxMove> m)
			{
				finished(m);
				prog.setVisible(false);
				solverBtn.setSelected(false);
			}
			
			protected void aborted()
			{
				prog.setVisible(false);
			}
		};
		
		SwingUtilities.invokeLater(new Runnable()
		{
			public void run()
			{
				prog.setVisible(true);
			}
		});
		
		solverAlg.solve();
	}
	
	public void stop()
	{
		solverAlg.abort();
	}
	
	public void finished(List<BoxMove> m)
	{
		if(m == null)
		{
			JOptionPane.showMessageDialog(gui.getTopLevelAncestor(),
							"The puzzle could not be solved.",
							"Whoops",
							JOptionPane.WARNING_MESSAGE);
		}
		else
		{
			JOptionPane.showMessageDialog(gui.getTopLevelAncestor(),
							"The puzzle has been solved.",
							"Done",
							JOptionPane.INFORMATION_MESSAGE);
			
			GridPuzzle puzzle = (GridPuzzle)gui.getPuzzle();
			
			puzzle.setNext(null);
			
			try
			{
				for(BoxMove move : m)
					puzzle.setLast(puzzle.last().applyMove(move));
			}
			catch(IllegalMoveException im)
			{
				puzzle.setNext(null);
			}
			
			gui.load(puzzle);
		}
	}
}
