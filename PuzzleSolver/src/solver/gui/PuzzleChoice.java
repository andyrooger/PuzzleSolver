package solver.gui;

import javax.swing.AbstractButton;
import javax.swing.JPanel;
import javax.swing.JLabel;
import javax.swing.JRadioButton;

import java.awt.BorderLayout;
import java.awt.GridLayout;

import solver.plugin.IPuzzleType;
import solver.plugin.PluginLoader;
import solver.utility.CancellableSelector;

public class PuzzleChoice extends JPanel
{
	public static final long serialVersionUID = 1;
	
	private SolverGUI gui;
	private int numchoices;
	private JPanel choices;
	private CancellableSelector<IPuzzleType> choiceButtons;
	
	public PuzzleChoice(final SolverGUI gui)
	{
		this.gui = gui;
		numchoices = 0;
		setLayout(new BorderLayout());
		add(new JLabel("Choose a puzzle type:"), BorderLayout.NORTH);
		choices = new JPanel();
		
		choiceButtons = new CancellableSelector<IPuzzleType>()
		{
      public boolean requestChange(IPuzzleType p)
      {
	      return gui.requestChangePuzzleType();
      }

      public AbstractButton createButton(String label)
      {
      	return new JRadioButton(label);
      }
      
      public void handleChange(IPuzzleType val)
      {
      	gui.changePuzzleType(val);
      }
		};
		
		createButtons();
		add(choices, BorderLayout.CENTER);
	}
	
	public IPuzzleType getPuzzle()
	{
		return choiceButtons.selected();
	}
	
	private void createButtons()
	{
		PluginLoader loader = new PluginLoader(gui.getBaseDir())
		{
			public void perPlugin(IPuzzleType p)
			{
				addPuzzleType(p);
			}
		};
		loader.loadPlugins(gui);
	}
	
	private void addPuzzleType(IPuzzleType type)
	{
		numchoices++;
		choices.setLayout(new GridLayout(numchoices, 1));
		choices.add(choiceButtons.get(type.getType(), type));
	}
}
