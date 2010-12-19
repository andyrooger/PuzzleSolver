package pushpuzzle.player;
import java.awt.BorderLayout;

import javax.swing.BorderFactory;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.KeyStroke;

import pushpuzzle.common.GridPuzzle;
import pushpuzzle.solver.PushSolver;

import solver.gui.SolverButton;
import solver.plugin.IPuzzle;
import solver.plugin.IPuzzlePane;
import solver.plugin.ISolver;


public class PushPlayer extends JPanel implements IPuzzlePane
{
	public static final long serialVersionUID = 1;
	
	private JScrollPane playArea;
	private PlayArea internalPlay;
	private NavBar nav;
	
	public JPanel getPanel()
	{
		return this;
	}
	
	public boolean start(IPuzzle p)
	{
		setLayout(new BorderLayout());
		setBorder(BorderFactory.createEmptyBorder(2, 2, 2, 2));
		
		nav = new NavBar();
		internalPlay = null;
		playArea = new JScrollPane();
		add(nav, BorderLayout.NORTH);
		add(playArea, BorderLayout.CENTER);
		
		if(p == null)
		{
			clean();
			return true;
		}
		else
			return load(p);
	}
	
	public boolean load(IPuzzle puzzle)
	{
		try
		{
			refreshPlayArea((GridPuzzle)puzzle);
		}
		catch(ClassCastException e)
		{
			JOptionPane.showMessageDialog(getTopLevelAncestor(),
			        "You are loading the wrong type of puzzle",
			        "Whoops", JOptionPane.INFORMATION_MESSAGE);
			return false;
		}
		
		return true;
	}
	
	public IPuzzle getPuzzle()
	{
		if(internalPlay == null)
			return null;
		else
			return internalPlay.getPuzzle();
	}
	
	public void saved()
	{
		if(internalPlay != null)
			internalPlay.saved();
	}
	
	public boolean changed()
	{
		if(internalPlay == null)
			return false;
		else
			return internalPlay.changed();
	}
	
	public void clean()
	{
		if(internalPlay != null)
			internalPlay.clean();
	}
	
	public ISolver getSolver(SolverButton b)
	{
		if(internalPlay != null)
			return new PushSolver(this, b);
		else
			return null;
	}
	
	public void end()
	{
		nav = null;
		internalPlay = null;
		playArea = null;
		removeAll();
	}
	
	public String getExt()
	{
		return "spp";
	}
	
	private void refreshPlayArea(GridPuzzle p)
	{
		replacePlayArea(new PlayArea(p, nav));
	}
	
	private void replacePlayArea(PlayArea p)
	{
		internalPlay = p;
		nav.setEditor(p);
		remove(playArea);
		playArea = new JScrollPane(p);
		playArea.getInputMap(WHEN_ANCESTOR_OF_FOCUSED_COMPONENT).put(KeyStroke.getKeyStroke("UP"), "none");
		playArea.getInputMap(WHEN_ANCESTOR_OF_FOCUSED_COMPONENT).put(KeyStroke.getKeyStroke("DOWN"), "none");
		playArea.getInputMap(WHEN_ANCESTOR_OF_FOCUSED_COMPONENT).put(KeyStroke.getKeyStroke("LEFT"), "none");
		playArea.getInputMap(WHEN_ANCESTOR_OF_FOCUSED_COMPONENT).put(KeyStroke.getKeyStroke("RIGHT"), "none");
		add(playArea, BorderLayout.CENTER);
		validate();
		repaint();
		p.madeVisible();
	}
}
