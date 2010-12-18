package solver.utility;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.AbstractButton;
import javax.swing.ButtonGroup;

public abstract class CancellableButtonGroup extends ButtonGroup
{
	public static final long serialVersionUID = 1;
	
	private ActionListener al;
	private AbstractButton lastSelected;
	
	public abstract boolean acceptChange(AbstractButton b);
	
	public CancellableButtonGroup()
	{
		al = new ActionListener()
		{
			public void actionPerformed(ActionEvent e)
			{
				if(e.getSource() == lastSelected)
					return;
				if(acceptChange((AbstractButton)e.getSource()))
				{
					fireActionPerformed(e);
					lastSelected = (AbstractButton)e.getSource();
				}
				else
				{
					if(lastSelected == null)
						clearSelection();
					else
						lastSelected.setSelected(true);
				}
			}
		};
		
		lastSelected = null;
		ehandler = null;
	}
	
	public void add(AbstractButton b)
	{
		b.addActionListener(al);
		super.add(b);
		if(getSelection() == b)
			lastSelected = b;
	}
	
	public void remove(AbstractButton b)
	{
		super.remove(b);
		b.removeActionListener(al);
	}
	
	public void setSelected(AbstractButton m)
	{
		super.setSelected(m.getModel(), true);
		lastSelected = m;
	}
	
	public void clearSelection()
	{
		super.clearSelection();
		lastSelected = null;
	}
	
	public AbstractButton selected()
	{
		return lastSelected;
	}
	
	private ActionListener ehandler;
	
	public void setActionListener(ActionListener l)
	{
		ehandler = l;
	}
	
	protected void fireActionPerformed(ActionEvent event)
	{
		ehandler.actionPerformed(event);
	}
}
