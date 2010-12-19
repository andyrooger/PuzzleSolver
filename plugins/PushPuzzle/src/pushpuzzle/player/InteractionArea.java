package pushpuzzle.player;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.GridLayout;
import java.awt.Rectangle;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.util.LinkedList;
import java.util.List;
import java.util.TreeSet;

import javax.swing.AbstractAction;
import javax.swing.ImageIcon;
import javax.swing.InputMap;
import javax.swing.JButton;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.KeyStroke;
import javax.swing.Timer;
import javax.swing.border.EmptyBorder;
import javax.swing.border.LineBorder;

import pushpuzzle.common.GridPuzzle;
import pushpuzzle.common.PuzzleCreateException;
import pushpuzzle.common.PuzzleState;
import solver.utility.Coords;
import solver.utility.Direction;
import solver.utility.ai.PathFinder;

public class InteractionArea extends JPanel
{
	public static final long serialVersionUID = 1;
	
	private JButton[][] btns;
	private GridPuzzle puzzle;
	private ImageIcon boxIcon;
	private ImageIcon playerIcon;
	
	public InteractionArea(GridPuzzle p)
	{
		puzzle = p;
		
		boxIcon = new ImageIcon(getClass().getResource("/images/Box.png"));
		playerIcon = new ImageIcon(getClass().getResource("/images/Player.png"));
		
		int iconSize = boxIcon.getIconHeight();
		if(boxIcon.getIconWidth() > iconSize)
			iconSize = boxIcon.getIconWidth();
		if(playerIcon.getIconHeight() > iconSize)
			iconSize = playerIcon.getIconHeight();
		if(playerIcon.getIconWidth() > iconSize)
			iconSize = playerIcon.getIconWidth();
		
		setLayout(new GridLayout(p.dims().getRows(), p.dims().getCols()));
		btns = new JButton[p.dims().getCols()][p.dims().getRows()];
		
		for(Coords c : p.dims())
		{
			JButton b = new JButton();
			btns[c.getCol()][c.getRow()] = b;

			Dimension btnSize = new Dimension(iconSize+10, iconSize+10);
			b.setSize(btnSize);
			b.setPreferredSize(btnSize);
			
			b.setFocusable(false);
			
			if(p.wall(c))
				b.setBackground(Color.BLUE);
			else
				b.setBackground(Color.WHITE);
			
			if(p.targets().contains(c))
				b.setBorder(new LineBorder(Color.RED, 5));
			else
				b.setBorder(new EmptyBorder(5, 5, 5, 5));
			
			
			b.addActionListener(new ClickListener(c));
			InputMap iMap = getInputMap(WHEN_IN_FOCUSED_WINDOW);
			iMap.put(KeyStroke.getKeyStroke(KeyEvent.VK_LEFT, 0, true), "mv_left");
			iMap.put(KeyStroke.getKeyStroke(KeyEvent.VK_RIGHT, 0, true), "mv_right");
			iMap.put(KeyStroke.getKeyStroke(KeyEvent.VK_UP, 0, true), "mv_up");
			iMap.put(KeyStroke.getKeyStroke(KeyEvent.VK_DOWN, 0, true), "mv_down");
			getActionMap().put("mv_left", new ArrowListener(Direction.WEST));
			getActionMap().put("mv_right", new ArrowListener(Direction.EAST));
			getActionMap().put("mv_up", new ArrowListener(Direction.NORTH));
			getActionMap().put("mv_down", new ArrowListener(Direction.SOUTH));
			add(b);
		}
		
		update();
	}
	
	protected void change()
	{
		// Overwritten when used to signal a change has been made here
	}
	
	public void update()
	{
		if(puzzle == null || puzzle.current() == null)
			return;
		
		for(Coords c : puzzle.dims())
		{
			JButton btn = btns[c.getCol()][c.getRow()];
			
			btn.setEnabled(puzzle.current().accessible(c));
			
			if(puzzle.current().player().equals(c))
				btn.setIcon(playerIcon);
			else if(puzzle.current().boxes().contains(c))
			{
				btn.setIcon(boxIcon);
				btn.setEnabled(true);
			}
			else
				btn.setIcon(null);
		}
		
		centreOn(btns[puzzle.current().player().getCol()][puzzle.current().player().getRow()]);
	}
	
	private void centreOn(JButton b)
	{
		int borderCells = 2;
		Rectangle r = b.getBounds();
		Rectangle space = new Rectangle(
						r.x-(r.width*borderCells),
						r.y-(r.height*borderCells),
						r.width*(1+2*borderCells),
						r.height*(1+2*borderCells));
		scrollRectToVisible(space);
	}
	
	public void moveTo(Coords c)
	{
		setEnabled(false);
		PathFinder p = new PathFinder(puzzle.current().accessibility(), puzzle.current().player(), c)
		{
      protected void aborted()
      {
      	setEnabled(true);
      }

      protected void solved(List<Direction> moves)
      {
      	final LinkedList<Direction> dirs = new LinkedList<Direction>(moves);
      	if(moves != null)
      	{
      		final Timer t = new Timer(100, null);
      		t.addActionListener(new ActionListener()
      		{
      			public void actionPerformed(ActionEvent arg0)
            {
              if(dirs.isEmpty())
              	t.stop();
              else
              	move(dirs.removeFirst());
            }
      		});
      			
      		t.setInitialDelay(0);
      		t.start();
      	}
      	setEnabled(true);
      }
		};
		p.solve();
	}
	
	public void move(Direction d)
	{
		Coords nPos = puzzle.current().player().adj(d);
		
		if(puzzle.current().accessible(nPos))
		{
			try
			{
				puzzle.setCurrent(nPos, puzzle.current().boxes());
				update();
				change();
			}
			catch(PuzzleCreateException e){}
		}
		else if(puzzle.current().boxes().contains(nPos))
		{
			Coords boxTo = nPos.adj(d);
			if(!puzzle.wall(boxTo) && !puzzle.current().boxes().contains(boxTo))
			{
				TreeSet<Coords> nBoxes = new TreeSet<Coords>(puzzle.current().boxes());
				nBoxes.remove(nPos);
				nBoxes.add(boxTo);
				try
				{
					puzzle.setNext(new PuzzleState(puzzle, nBoxes, nPos));
					puzzle.next();
					update();
					change();
					if(puzzle.targets().contains(boxTo))
					{
						if(puzzle.current().goal())
						{
							JOptionPane.showMessageDialog(getTopLevelAncestor(),
							        "Well I never. You've done it!",
							        "Congratuwelldone!", JOptionPane.INFORMATION_MESSAGE);
						}
					}
				}
				catch(PuzzleCreateException e)
				{
					e.printStackTrace();
				}
			}
		}
	}
	
	private class ClickListener implements ActionListener
	{
		private Coords coords;
		
		public ClickListener(Coords c)
		{
			coords = c;
		}
		
		public void actionPerformed(ActionEvent e)
		{
			if(puzzle.current().accessible(coords))
				moveTo(coords);
		}
	}
	
	private class ArrowListener extends AbstractAction
	{
		public static final long serialVersionUID = 1;
		private Direction dir;
		
		public ArrowListener(Direction d)
		{
			dir = d;
		}
		
    public void actionPerformed(ActionEvent e)
    {
    	move(dir);
    }
	}
}
