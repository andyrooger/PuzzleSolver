package pushpuzzle.creator;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.TreeSet;

import javax.swing.BorderFactory;
import javax.swing.Icon;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JOptionPane;
import javax.swing.JPanel;

import pushpuzzle.common.GridPuzzle;
import pushpuzzle.common.PuzzleCreateException;
import solver.utility.BoolMap;
import solver.utility.Coords;
import solver.utility.Dimensions;


public abstract class CreationArea extends JPanel
{
	public static final long serialVersionUID = 1;
	
	private Dimensions dims;
	private Coords player;
	private ImageIcon boxIcon;
	private ImageIcon playerIcon;
	private int tileSize;
	private EditTile[][] tiles;
	private boolean changed;
	
	public abstract EditMode getCreateMode();
	
	public CreationArea(Dimensions d)
	{
		init(d);
	}
	
	public CreationArea(GridPuzzle p)
	{
		p.restart();
		init(p.dims());
		for(Coords c : p.dims())
		{
			if(p.wall(c))
				tiles[c.getCol()][c.getRow()].setContent(EditMode.WALL);
		}
		for(Coords c : p.targets())
			tiles[c.getCol()][c.getRow()].setTarget(true);
		
		for(Coords c : p.current().boxes())
			tiles[c.getCol()][c.getRow()].setContent(EditMode.BOX);
		player = p.current().player();
		tiles[player.getCol()][player.getRow()].setContent(EditMode.PLAYER);
	}
	
	private void init(Dimensions d)
	{
		dims = d;
		changed = false;
		
		setLayout(new GridLayout(d.getRows(), d.getCols()));
		
		loadIcons();
		
		tiles = new EditTile[d.getCols()][d.getRows()];
		
		for(Coords c : d)
		{
			tiles[c.getCol()][c.getRow()] = new EditTile(c);
			add(tiles[c.getCol()][c.getRow()]);
		}
	}
	
	private void loadIcons()
	{
		boxIcon = new ImageIcon(getClass().getResource("/images/Box.png"));
		tileSize = boxIcon.getIconHeight();
		if(boxIcon.getIconWidth() > tileSize)
			tileSize = boxIcon.getIconWidth();
		playerIcon = new ImageIcon(getClass().getResource("/images/Player.png"));
		if(playerIcon.getIconWidth() > tileSize)
			tileSize = playerIcon.getIconWidth();
		if(playerIcon.getIconHeight() > tileSize)
			tileSize = playerIcon.getIconHeight();
	}
	
	public void saved()
	{
		changed = false;
	}
	
	public boolean changed()
	{
		return changed;
	}
	
	public GridPuzzle getPuzzle()
	{
		if(player == null)
		{
			JOptionPane.showMessageDialog(getTopLevelAncestor(),
			        "There is no player on the board",
			        "Whoops", JOptionPane.INFORMATION_MESSAGE);
			return null;
		}
		
		BoolMap map = new BoolMap(dims, true);
		TreeSet<Coords> targets = new TreeSet<Coords>();
		TreeSet<Coords> boxes = new TreeSet<Coords>();
		
		for(Coords c : dims)
		{
			EditTile tile = tiles[c.getCol()][c.getRow()];
			
			if(tile.holds() != EditMode.WALL)
				map.set(c, false);
			
			if(tile.target())
				targets.add(c);
			
			if(tile.holds() == EditMode.BOX)
				boxes.add(c);
		}
		
		if(targets.size() != boxes.size())
		{
			JOptionPane.showMessageDialog(getTopLevelAncestor(),
			        "There are a different number of targets than boxes",
			        "Whoops", JOptionPane.INFORMATION_MESSAGE);
			return null;
		}
		
		GridPuzzle r = null;
		try
		{
			r = new GridPuzzle(map, targets, boxes, player);
		}
		catch(PuzzleCreateException e)
		{
			JOptionPane.showMessageDialog(getTopLevelAncestor(),
			        "There was a problem creating your puzzle: "+e.getMessage(),
			        "Whoops", JOptionPane.INFORMATION_MESSAGE);
			return null;
		}
		
		return r;
	}
	
	private class EditTile extends JButton implements ActionListener
	{
		public static final long serialVersionUID = 1;
		private Coords pos;
		private EditMode content;
		private boolean target;
		
		public EditTile(Coords c)
		{
			super();
			setSize(tileSize+10, tileSize+10);
			setPreferredSize(new Dimension(tileSize+10, tileSize+10));
			setMaximumSize(new Dimension(tileSize+10, tileSize+10));
			setMinimumSize(new Dimension(tileSize+10, tileSize+10));
			this.pos = c;
			content = EditMode.EMPTY;
			target = false;
			setAppearance();
			addActionListener(this);
		}
		
		public EditMode holds()
		{
			return content;
		}
		
		public boolean target()
		{
			return target;
		}
		
		private void setAppearance()
		{
			Icon icon = null;
			Color background = new Color(255,255,255);
			
			switch(content)
			{
				case EMPTY:
					break;
				case BOX:
					icon = boxIcon;
					break;
				case PLAYER:
					if(pos.equals(player))
						icon = playerIcon;
					else
					{
						content = EditMode.EMPTY;
						setAppearance();
						return;
					}
					break;
				case WALL:
					background = new Color(0,0,160);
					break;
				default:
					break;
			}
			
			setIcon(icon);
			setBackground(background);
			
			if(target)
				setBorder(BorderFactory.createLineBorder(Color.RED, 5));
			else
				setBorder(BorderFactory.createLineBorder(Color.BLACK, 5));
		}

		public void setContent(EditMode content)
		{
			this.content = content;
			setAppearance();
		}
		
		public void setTarget(boolean b)
		{
			target = b;
			setAppearance();
		}
		
    public void actionPerformed(ActionEvent e)
    {
    	if(getCreateMode() == null)
    	{
    		JOptionPane.showMessageDialog(getTopLevelAncestor(),
				        "You must choose what to change before changing it here.",
				        "Whoops", JOptionPane.INFORMATION_MESSAGE);
    		return;
    	}
    	
    	changed = true;
    	
    	switch(getCreateMode())
    	{
    		case BOX:
    			if(content == EditMode.BOX)
    				setContent(EditMode.EMPTY);
    			else
    			{
    				if(pos.equals(player))
    					player = null;
    				setContent(EditMode.BOX);
    			}
    			break;
    		case EMPTY:
    			if(pos.equals(player))
    				player = null;
    			setContent(EditMode.EMPTY);
    			break;
    		case PLAYER:
    			if(pos.equals(player))
    			{
    				player = null;
    				setContent(EditMode.EMPTY);
    			}
    			else
    			{
    				if(player != null)
    				{
    					Coords oldPos = player;
    					tiles[oldPos.getCol()][oldPos.getRow()].setContent(EditMode.EMPTY);
    				}
  					player = pos;
  					setContent(EditMode.PLAYER);
    			}
    			break;
    		case TARGET:
    			target = !target;
    			if(content == EditMode.WALL)
    				setContent(EditMode.EMPTY);
    			else
    				setAppearance();
    			break;
    		case WALL:
    			if(content == EditMode.WALL)
    				setContent(EditMode.EMPTY);
    			else
    			{
    				if(pos.equals(player))
    					player = null;
    				target = false;
    				setContent(EditMode.WALL);
    			}
    			break;
    	}
    }
	}
}
