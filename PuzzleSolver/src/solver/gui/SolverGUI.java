package solver.gui;

import java.awt.BorderLayout;
import java.awt.HeadlessException;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;

import solver.plugin.IPuzzle;
import solver.plugin.IPuzzlePane;
import solver.plugin.IPuzzleType;

public class SolverGUI extends JFrame
{
	public static final long serialVersionUID = 1;
	
	private static final String appTitle = "Puzzle Solver";
	private String baseDir;
	
	private PuzzleChoice puzzleChoice;
	private ModeChoice modeChoice;
	private ControlPanel ctrlPnl;
	private SolverButton solverBtn;
	
	public SolverGUI(String baseDir) throws HeadlessException
	{
		this.baseDir = baseDir;
		
		setTitle(appTitle);
		setSize(800, 800);
		setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
		
		ctrlPnl = new ControlPanel(this);
		ctrlPnl.setEnabled(false);
		puzzleChoice = new PuzzleChoice(this);
		modeChoice = new ModeChoice(this);
		modeChoice.setEnabled(false);
		solverBtn = new SolverButton();
		solverBtn.setSelected(false);
		solverBtn.setEnabled(false);
		
		JPanel topPanel = new JPanel(new BorderLayout());
		topPanel.add(modeChoice, BorderLayout.CENTER);
		topPanel.add(solverBtn, BorderLayout.EAST);
		getContentPane().add(puzzleChoice, BorderLayout.WEST);
		getContentPane().add(topPanel, BorderLayout.NORTH);
		getContentPane().add(ctrlPnl, BorderLayout.SOUTH);
		JPanel placeholder = new JPanel();
		placeholder.add(new JLabel("No puzzle type is currently selected"));
		getContentPane().add(placeholder, BorderLayout.CENTER);
		
		addWindowListener(new WindowAdapter()
		{
			public void windowClosing(WindowEvent e)
			{
				killApp();
			}
		});
		
		setVisible(true);
	}
	
	public String getBaseDir()
	{
		return baseDir;
	}
	
	public boolean requestChangePuzzleType()
	{
		solverBtn.setSelected(false);
		return (getPane() == null) || (new PuzzleSaver(getPane())).check(this);
	}
	
	public void changePuzzleType(IPuzzleType type)
	{
		setTitle(appTitle + " - " + type.getType());
		modeChoice.setMode(PuzzleMode.CREATE);
		swapPanels(getPane(type, PuzzleMode.CREATE), null);
		setModeControls(PuzzleMode.CREATE);
	}
	
	public boolean requestChangePuzzleMode()
	{
		solverBtn.setSelected(false);
		return (getPane() == null) || (new PuzzleSaver(getPane())).check(this);
	}
	
	public void changePuzzleMode(PuzzleMode mode)
	{
		setModeControls(mode);
		if(getPane(mode).getExt() != null && getPane().getPuzzle() != null)
			swapPanels(getPane(mode), getPane().getPuzzle());
		else
			swapPanels(getPane(mode), null);
	}
	
	private void setModeControls(PuzzleMode mode)
	{
		modeChoice.setEnabled(true);
		ctrlPnl.setEnabled(true);
		// Change controls for this mode
	}
	
	private void swapPanels(IPuzzlePane pane, IPuzzle nPuzzle)
	{
		// Remove old stuff
		if(getPane() != null)
			getPane().end();
		getContentPane().remove(getContentPane().getComponentCount()-1);
		
		// add new stuff
		getContentPane().add(pane.getPanel(), BorderLayout.CENTER);
		pane.start(nPuzzle);
		setSolver(pane);
		getContentPane().validate();
		pane.getPanel().repaint();
	}
	
	private IPuzzlePane getPane(IPuzzleType type, PuzzleMode mode)
	{
		if(type == null || mode == null)
			return null;
		else
			return type.get(mode);
	}
	
	private IPuzzlePane getPane(PuzzleMode mode)
	{
		return getPane(puzzleChoice.getPuzzle(), mode);
	}
	
	public IPuzzlePane getPane()
	{
		return getPane(modeChoice.getMode());
	}
	
	private void killApp()
	{
		solverBtn.setSelected(false);
		if((getPane() == null) || (new PuzzleSaver(getPane())).check(this))
		{
			System.exit(0);
		}
	}
	
	public void setSolver(IPuzzlePane s)
	{
		solverBtn.setSolver(s.getSolver(solverBtn));
	}
}
