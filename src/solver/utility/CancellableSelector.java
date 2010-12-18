package solver.utility;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.HashMap;
import java.util.Map;

import javax.swing.AbstractButton;


public abstract class CancellableSelector<T>
{
	private CancellableButtonGroup grp;
	private Map<AbstractButton, T> btnMap;
	
	protected abstract boolean requestChange(T val);
	protected abstract void handleChange(T val);
	protected abstract AbstractButton createButton(String label);
	
	public CancellableSelector()
	{
		btnMap = new HashMap<AbstractButton, T>();
		
		grp = new CancellableButtonGroup()
		{
			public static final long serialVersionUID = 1;
			
			public boolean acceptChange(AbstractButton b)
			{
				return requestChange(btnMap.get(b));
			}
		};
		
		grp.setActionListener(new ActionListener()
		{
			public void actionPerformed(ActionEvent e)
			{
				handleChange(btnMap.get(e.getSource()));
			}
		});
	}
	
	public AbstractButton get(String label, T val)
	{
		AbstractButton b = createButton(label);
		grp.add(b);
		btnMap.put(b, val);
		
		return b;
	}
	
	public T selected()
	{
		return btnMap.get(grp.selected());
	}
	
	public void selected(T val)
	{
		for(AbstractButton b : btnMap.keySet())
		{
			if(btnMap.get(b) == val)
			{
				grp.setSelected(b);
				break;
			}
		}
	}
	
	public void setEnabled(boolean b)
	{
		for(AbstractButton btn : btnMap.keySet())
			btn.setEnabled(b);
	}
}
