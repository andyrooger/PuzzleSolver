package pushpuzzle.creator;

import java.awt.BorderLayout;
import java.awt.GridLayout;
import java.awt.Window;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.EnumMap;
import java.util.Map;

import javax.swing.BorderFactory;
import javax.swing.ButtonGroup;
import javax.swing.ButtonModel;
import javax.swing.Icon;
import javax.swing.ImageIcon;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JToggleButton;

import pushpuzzle.common.GridPuzzle;

import solver.gui.SolverButton;
import solver.plugin.IPuzzle;
import solver.plugin.IPuzzlePane;
import solver.plugin.ISolver;
import solver.utility.Dimensions;


public class PushCreator extends JPanel implements IPuzzlePane
{
	public static final long serialVersionUID = 1;
	
	private JScrollPane creationArea;
	private CreationArea internalCreation;
	
	public JPanel getPanel()
	{
		return this;
	}
	
	public boolean start(IPuzzle p)
	{
		setLayout(new BorderLayout());
		setBorder(BorderFactory.createEmptyBorder(2, 2, 2, 2));
		
		internalCreation = null;
		creationArea = new JScrollPane();
		add(creationArea, BorderLayout.CENTER);
		add(creationControlPanel(), BorderLayout.SOUTH);
		
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
			refreshCreationArea((GridPuzzle)puzzle);
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
		return internalCreation.getPuzzle();
	}
	
	public void saved()
	{
		internalCreation.saved();
	}
	
	public boolean changed()
	{
		return internalCreation.changed();
	}
	
	public void clean()
	{
		new SizePicker((Window)this.getTopLevelAncestor())
		{
			public static final long serialVersionUID = 1;
			
			public void chosen(Dimensions d)
			{
				refreshCreationArea(d);
			}
		};
	}
	
	public ISolver getSolver(SolverButton b)
	{
		return null;
	}
	
	public void end()
	{
		internalCreation = null;
		creationArea = null;
		removeAll();
	}
	
	public String getExt()
	{
		return "spp";
	}
	
	private void refreshCreationArea(Dimensions d)
	{
		replaceCreationArea(new CreationArea(d){
			public static final long serialVersionUID = 1;
			public EditMode getCreateMode()
			{
				return creationControlPanel().getMode();
			}
		});
	}
	
	private void refreshCreationArea(GridPuzzle p)
	{
		replaceCreationArea(new CreationArea(p){
			public static final long serialVersionUID = 1;
			public EditMode getCreateMode()
			{
				return creationControlPanel().getMode();
			}
		});
	}
	
	private void replaceCreationArea(CreationArea p)
	{
		internalCreation = p;
		remove(creationArea);
		creationArea = new JScrollPane(p);
		add(creationArea, BorderLayout.CENTER);
		validate();
		repaint();
	}
	
	private ControlPanel ctrlPnl = null;
	
	private ControlPanel creationControlPanel()
	{
		if(ctrlPnl == null)
			ctrlPnl = new ControlPanel();
		return ctrlPnl;
	}
	
	public Icon getModeIcon(EditMode mode)
	{
		return new ImageIcon(getClass().getResource("/images/"+mode.toString()+".png"));
	}
	
	private class ControlPanel extends JPanel
	{
		public static final long serialVersionUID = 1;
		
		private EditMode mode;
		private Map<EditMode, ButtonModel> buttons;
		
		public ControlPanel()
    {
			super();
			mode = null;
			ButtonGroup btnGrp = new ButtonGroup();
			buttons = new EnumMap<EditMode, ButtonModel>(EditMode.class);
			
			setLayout(new GridLayout(1, EditMode.values().length));
			
			for(final EditMode m : EditMode.values())
			{
				JToggleButton btn = new JToggleButton(getModeIcon(m));
				btn.setToolTipText("Edit "+m.toString());
				btn.addActionListener(new ActionListener()
				{
					public void actionPerformed(ActionEvent arg0)
					{
						mode = m;
					}
				});
				btnGrp.add(btn);
				buttons.put(m, btn.getModel());
				add(btn);
			}
    }
		
		public EditMode getMode()
		{
			return mode;
		}
		
		/*
		public void setMode(EditMode mode)
		{
			buttons.get(mode).setSelected(true);
			this.mode = mode;
		}
		*/
	}
}
