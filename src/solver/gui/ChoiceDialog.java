package solver.gui;

import java.awt.BorderLayout;
import java.awt.Frame;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.HashSet;
import java.util.Set;

import javax.swing.JButton;
import javax.swing.JComponent;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JToggleButton;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

public class ChoiceDialog<CType> extends JDialog
{
	public static final long serialVersionUID = 1;
	
	private final boolean multiple;
	private JPanel btnPanel;
	private int choices;
	private HashSet<CType> chosen;
	private CType choice;
	
	public ChoiceDialog(Frame owner, String title, boolean multiple)
	{
		super(owner, title, true);
		
		this.multiple = multiple;
		choices = 0;
		if(multiple)
			chosen = new HashSet<CType>();
		choice = null;
		
		setLayout(new BorderLayout());
		
		add(new JLabel(title), BorderLayout.NORTH);
		
		btnPanel = new JPanel();
		btnPanel.setLayout(new GridLayout(0, 1));
		add(btnPanel, BorderLayout.CENTER);
		
		if(multiple)
		{
			JButton ok = new JButton("OK");
			ok.addActionListener(new ActionListener()
			{
				public void actionPerformed(ActionEvent arg0)
				{
					setVisible(false);
				}
			});
			add(ok, BorderLayout.SOUTH);
		}
		
		pack();
	}
	
	public void addChoice(final String text, final CType ret)
	{
		choices++;
		
		JComponent comp;
		
		if(multiple)
		{
			final JToggleButton btn = new JToggleButton(text);
			btn.addChangeListener(new ChangeListener()
			{
				public void stateChanged(ChangeEvent ce)
				{
					if(btn.isSelected())
						chosen.add(ret);
					else
						chosen.remove(ret);
				}
			});
			comp = btn;
		}
		else
		{
			JButton btn = new JButton(text);
			btn.addActionListener(new ActionListener()
			{
				public void actionPerformed(ActionEvent arg0)
				{
					choice = ret;
					setVisible(false);
				}
			});
			comp = btn;
		}
		
		btnPanel.setLayout(new GridLayout(choices, 1));
		btnPanel.add(comp);
		pack();
	}
	
	public CType getChoice()
	{
		if(multiple || choices == 0)
			return null;
		setVisible(true);
		return choice;
	}
	
	public Set<CType> getChoices()
	{
		if(!multiple || choices == 0)
			return null;
		setVisible(true);
		return chosen;
	}
}
