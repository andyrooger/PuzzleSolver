package solver.gui;

import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;

import javax.swing.JOptionPane;
import javax.swing.JToggleButton;

import solver.plugin.ISolver;

public class SolverButton extends JToggleButton
{
	public static final long serialVersionUID = 1;
	
	private ISolver solver;
	private boolean started;
	
	SolverButton()
	{
		super("Solve");
		solver = null;
		started = false;
		addItemListener(new ItemListener()
		{
			public void itemStateChanged(ItemEvent e)
			{
				stateChanged(e.getStateChange() == ItemEvent.SELECTED);
			}
		});
	}
	
	public void setSolver(ISolver s)
	{
		setSelected(false);
		setEnabled(s != null);
		solver = s;
	}
	
	public void setSelected(boolean b)
	{
		super.setSelected(b);
		stateChanged(b);
	}
	
	private void stateChanged(boolean s)
	{
		if(started != s)
		{
			started = s;
			if(solver != null)
			{
				if(started)
					solver.start();
				else
					solver.stop();
			}
			
			if(started && solver == null)
			{
				JOptionPane.showMessageDialog(getTopLevelAncestor(),
				        "This type of puzzle cannot be solved yet.",
				        "Whoops", JOptionPane.INFORMATION_MESSAGE);
				setSelected(false);
			}
		}
	}
}
