package solver.gui;

import java.awt.Component;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JPanel;

public class ControlPanel extends JPanel
{
	public static final long serialVersionUID = 1;
	
	public ControlPanel(final SolverGUI gui)
	{
		setLayout(new GridLayout(1, 3));
		
		JButton clean = new JButton("Clean");
		clean.addActionListener(new ActionListener()
		{
			public void actionPerformed(ActionEvent arg0)
			{
				PuzzleSaver ps = new PuzzleSaver(gui.getPane());
				if(ps.check(gui))
				{
					gui.getPane().clean();
					gui.setSolver(gui.getPane());
				}
			}
		});
		add(clean);
		
		JButton save = new JButton("Save");
		save.addActionListener(new ActionListener()
		{
			public void actionPerformed(ActionEvent arg0)
			{
				(new PuzzleSaver(gui.getPane())).save(gui);
			}
		});
		add(save);
		
		JButton load = new JButton("Load");
		load.addActionListener(new ActionListener()
		{
			public void actionPerformed(ActionEvent arg0)
			{
				PuzzleSaver ps = new PuzzleSaver(gui.getPane());
				if(ps.check(gui))
				{
					ps.load(gui);
					gui.setSolver(gui.getPane());
				}
			}
		});
		add(load);
	}
	
	public void setEnabled(boolean b)
	{
		for(Component c : getComponents())
			c.setEnabled(b);
	}
}
