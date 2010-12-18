import java.util.EnumMap;

import javax.swing.JLabel;
import javax.swing.JPanel;

import solver.gui.PuzzleMode;
import solver.gui.SolverButton;
import solver.plugin.IPuzzle;
import solver.plugin.IPuzzlePane;
import solver.plugin.IPuzzleType;
import solver.plugin.ISolver;

public class ConcretePuzzleType implements IPuzzleType
{
	private int i;
	private EnumMap<PuzzleMode, IPuzzlePane> panes;
	
	public ConcretePuzzleType()
	{
		this.i = 1;
		panes = new EnumMap<PuzzleMode, IPuzzlePane>(PuzzleMode.class);
		System.out.println("Init puzzle "+this.hashCode());
	}
	
	public String getType()
	{
		System.out.println("Get type "+this.hashCode());
		return "Concrete Puzzle: "+i;
	}
	
	public IPuzzlePane get(PuzzleMode mode)
	{
		System.out.println("Get panel "+this.hashCode());
		if(panes.get(mode) == null)
		{
			switch(mode)
			{
				case CREATE:
					panes.put(mode, new ConcreteCreator());
					break;
				case PLAY:
					panes.put(mode, new ConcretePlayer());
					break;
			}
		}
		
		return panes.get(mode);
	}
	
	private class ConcreteCreator extends JPanel implements IPuzzlePane
	{
		public static final long serialVersionUID = 1;
		
		ConcreteCreator()
		{
			super();
			add(new JLabel("Creator: "+i));
			System.out.println("Init creator "+this.hashCode());
		}
		
		public JPanel getPanel()
		{
			System.out.println("Get creator "+this.hashCode());
			return this;
		}
		
		public boolean start(IPuzzle p)
		{
			System.out.println("Start creator "+this.hashCode());
			return true;
		}
		
		public boolean load(IPuzzle puzzle)
		{
			System.out.println("Load puzzle "+this.hashCode());
			return false;
		}
		
		public IPuzzle getPuzzle()
		{
			System.out.println("Get puzzle "+this.hashCode());
			return null;
		}
		
		public void clean()
		{
			System.out.println("Clean creator "+this.hashCode());
		}
		
		public void saved()
		{
			System.out.println("Been saved "+this.hashCode());
		}
		
		public boolean changed()
		{
			System.out.println("Is changed "+this.hashCode());
			return true;
		}
		
		public ISolver getSolver(SolverButton b)
		{
			System.out.println("Get null solver "+this.hashCode());
			return null;
		}
		
		public void end()
		{
			System.out.println("End creator "+this.hashCode());
		}
		
		public String getExt()
		{
			System.out.println("Get extension "+this.hashCode());
			return null;
		}
	}
	
	private class ConcretePlayer extends JPanel implements IPuzzlePane
	{
		public static final long serialVersionUID = 1;
		
		ConcretePlayer()
		{
			super();
			add(new JLabel("Player: "+i));
			System.out.println("Init player "+this.hashCode());
		}
		
		public JPanel getPanel()
		{
			System.out.println("Get player "+this.hashCode());
			return this;
		}
		
		public boolean start(IPuzzle p)
		{
			System.out.println("Start player "+this.hashCode());
			return true;
		}
		
		public boolean load(IPuzzle state)
		{
			System.out.println("Load puzzle "+this.hashCode());
			return false;
		}
		
		public IPuzzle getPuzzle()
		{
			System.out.println("Get puzzle "+this.hashCode());
			return null;
		}
		
		public void saved()
		{
			System.out.println("Been saved "+this.hashCode());
		}
		
		public boolean changed()
		{
			System.out.println("Check if changed "+this.hashCode());
			return false;
		}
		
		public void clean()
		{
			System.out.println("Clean play area "+this.hashCode());
		}
		
		public ISolver getSolver(SolverButton b)
		{
			return new ISolver()
			{
				public void stop()
				{
					System.out.println("Stop solver "+this.hashCode());
				}
				
				public void start()
				{
					System.out.println("Start solver "+this.hashCode());
				}
			};
		}
		
		public void end()
		{
			System.out.println("End player "+this.hashCode());
		}
		
		public String getExt()
		{
			return null;
		}
	}
}