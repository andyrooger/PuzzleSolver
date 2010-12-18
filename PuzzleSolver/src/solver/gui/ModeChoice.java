package solver.gui;

import java.awt.GridLayout;

import javax.swing.AbstractButton;
import javax.swing.JToggleButton;
import javax.swing.JPanel;

import solver.utility.CancellableSelector;

public class ModeChoice extends JPanel
{
	public static final long serialVersionUID = 1;
	
	private CancellableSelector<PuzzleMode> btnGrp;
	
	public ModeChoice(final SolverGUI gui)
  {
		btnGrp = new CancellableSelector<PuzzleMode>()
		{
			protected boolean requestChange(PuzzleMode val)
			{
				return gui.requestChangePuzzleMode();
			}
			
			protected void handleChange(PuzzleMode val)
			{
				gui.changePuzzleMode(val);
			}
			
			protected AbstractButton createButton(String label)
			{
				return new JToggleButton(label);
			}
		};
		
		setLayout(new GridLayout(1, PuzzleMode.values().length));
		
		for(PuzzleMode mode : PuzzleMode.values())
			add(btnGrp.get(mode.toString(), mode));
  }
	
	public PuzzleMode getMode()
	{
		return btnGrp.selected();
	}
	
	public void setMode(PuzzleMode mode)
	{
		btnGrp.selected(mode);
	}
	
	public void setEnabled(boolean e)
	{
		btnGrp.setEnabled(e);
	}
}
