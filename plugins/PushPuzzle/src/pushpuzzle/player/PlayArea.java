package pushpuzzle.player;

import javax.swing.JPanel;

import pushpuzzle.common.GridPuzzle;

public class PlayArea extends JPanel
{
	public static final long serialVersionUID = 1;
	
	private boolean changed;
	private GridPuzzle puzzle;
	private InteractionArea view;
	private NavBar nav;
	
	public PlayArea(GridPuzzle p, final NavBar nav)
	{
		if(p == null || nav == null)
			throw new NullPointerException();
		puzzle = p;
		this.nav = nav;
		changed = false;
		view = new InteractionArea(p)
		{
			public static final long serialVersionUID = 1;
			protected void change()
			{
				changed = true;
				nav.setAppearance();
			}
		};
		add(view);
	}
	
	public void next()
	{
		puzzle.next();
		nav.setAppearance();
		view.update();
	}
	
	public void previous()
	{
		puzzle.previous();
		nav.setAppearance();
		view.update();
	}
	
	public boolean hasNext()
	{
		return puzzle.hasNext();
	}
	
	public boolean hasPrevious()
	{
		return puzzle.hasPrevious();
	}
	
	public void clean()
	{
		puzzle.restart();
		nav.setAppearance();
		view.update();
	}
	
	public boolean changed()
	{
		return changed;
	}
	
	public void saved()
	{
		changed = false;
	}
	
	public GridPuzzle getPuzzle()
	{
		return puzzle;
	}
	
	public void madeVisible()
	{
		view.update();
	}
}
