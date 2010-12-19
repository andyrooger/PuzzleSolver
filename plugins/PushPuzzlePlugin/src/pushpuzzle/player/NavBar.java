package pushpuzzle.player;

import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JPanel;

public class NavBar extends JPanel
{
	public static final long serialVersionUID = 1;
	
	private JButton lbutton;
	private JButton rbutton;
	private PlayArea editor;
	
	public NavBar()
	{
		editor = null;
		setLayout(new GridLayout(1, 2));
		ImageIcon larrow = new ImageIcon(getClass().getResource("/images/larrow.png"));
		ImageIcon rarrow = new ImageIcon(getClass().getResource("/images/rarrow.png"));
		lbutton = new JButton(larrow);
		rbutton = new JButton(rarrow);
		add(lbutton);
		add(rbutton);
		
		lbutton.addActionListener(new ActionListener()
		{
			public void actionPerformed(ActionEvent e)
			{
				if(editor == null)
					return;
				if(editor.hasPrevious())
					editor.previous();
			}
		});
		
		rbutton.addActionListener(new ActionListener()
		{
			public void actionPerformed(ActionEvent e)
			{
				if(editor == null)
					return;
				if(editor.hasNext())
					editor.next();
			}
		});
		
		setAppearance();
	}
	
	public void setAppearance()
	{
		if(editor == null)
		{
			lbutton.setEnabled(false);
			rbutton.setEnabled(false);
			return;
		}
		lbutton.setEnabled(editor.hasPrevious());
		rbutton.setEnabled(editor.hasNext());
	}
	
	public void setEditor(PlayArea p)
	{
		editor = p;
		setAppearance();
	}
}
